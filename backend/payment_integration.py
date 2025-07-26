"""
OBJX Intelligence Platform - Payment Integration System
Stripe integration for subscription management and tier upgrades
"""

import os
import json
import stripe
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from flask import current_app

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_placeholder')

class SubscriptionTier(Enum):
    """Subscription tier definitions"""
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    STAFF = "staff"
    ADMIN = "admin"

class PaymentStatus(Enum):
    """Payment status definitions"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class PricingPlan:
    """Pricing plan configuration"""
    tier: SubscriptionTier
    name: str
    description: str
    monthly_price: int  # in cents
    annual_price: int   # in cents
    features: List[str]
    stripe_price_id_monthly: str
    stripe_price_id_annual: str

@dataclass
class PaymentRecord:
    """Payment record structure"""
    payment_id: str
    user_id: str
    amount: int
    currency: str
    status: PaymentStatus
    tier: SubscriptionTier
    billing_period: str
    created_at: datetime
    updated_at: datetime
    stripe_payment_intent_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class PaymentIntegration:
    """Payment integration and subscription management"""
    
    def __init__(self):
        self.pricing_plans = self._initialize_pricing_plans()
        self.payment_records = {}  # In production, this would be a database
        
    def _initialize_pricing_plans(self) -> Dict[SubscriptionTier, PricingPlan]:
        """Initialize pricing plans for all tiers"""
        return {
            SubscriptionTier.TIER_1: PricingPlan(
                tier=SubscriptionTier.TIER_1,
                name="Foundation Methodology",
                description="Systematic thinking access with building code review",
                monthly_price=9900,  # $99/month
                annual_price=99900,  # $999/year (2 months free)
                features=[
                    "Systematic Thinking Access",
                    "Building/Municipal Code Review",
                    "Basic SDGE Calculator",
                    "Property Investment Analysis",
                    "Proposal Templates"
                ],
                stripe_price_id_monthly="price_tier1_monthly",
                stripe_price_id_annual="price_tier1_annual"
            ),
            SubscriptionTier.TIER_2: PricingPlan(
                tier=SubscriptionTier.TIER_2,
                name="Compound Intelligence",
                description="Personal memory + advanced systematic thinking",
                monthly_price=29900,  # $299/month
                annual_price=299900,  # $2999/year (2 months free)
                features=[
                    "All Tier 1 Features",
                    "Personal Memory System (Mem0)",
                    "Advanced Task Management",
                    "Google Workspace Integration",
                    "Research & Feasibility Studies",
                    "Priority Support"
                ],
                stripe_price_id_monthly="price_tier2_monthly",
                stripe_price_id_annual="price_tier2_annual"
            ),
            SubscriptionTier.TIER_3: PricingPlan(
                tier=SubscriptionTier.TIER_3,
                name="Complete Methodology",
                description="Full systematic thinking + team collaboration",
                monthly_price=59900,  # $599/month
                annual_price=599900,  # $5999/year (2 months free)
                features=[
                    "All Tier 2 Features",
                    "Complete Memory Analytics",
                    "Team Collaboration Tools",
                    "Advanced Project Management",
                    "Custom Integrations",
                    "White-label Options",
                    "Dedicated Support"
                ],
                stripe_price_id_monthly="price_tier3_monthly",
                stripe_price_id_annual="price_tier3_annual"
            ),
            SubscriptionTier.STAFF: PricingPlan(
                tier=SubscriptionTier.STAFF,
                name="Staff Access",
                description="Team member access with project management",
                monthly_price=19900,  # $199/month
                annual_price=199900,  # $1999/year (2 months free)
                features=[
                    "Project Management Hub",
                    "Task Coordination",
                    "Google Workspace Integration",
                    "Team Memory Access",
                    "Client Communication Tools"
                ],
                stripe_price_id_monthly="price_staff_monthly",
                stripe_price_id_annual="price_staff_annual"
            ),
            SubscriptionTier.ADMIN: PricingPlan(
                tier=SubscriptionTier.ADMIN,
                name="Admin Control",
                description="Complete business operations and team management",
                monthly_price=99900,  # $999/month
                annual_price=999900,  # $9999/year (2 months free)
                features=[
                    "All Features Included",
                    "Multi-Agent Orchestration",
                    "Business Intelligence",
                    "Billing & Proposals",
                    "User Management",
                    "QuickBooks Integration",
                    "Custom Development"
                ],
                stripe_price_id_monthly="price_admin_monthly",
                stripe_price_id_annual="price_admin_annual"
            )
        }
    
    def get_pricing_plans(self) -> Dict[str, Any]:
        """Get all pricing plans for frontend display"""
        plans = {}
        for tier, plan in self.pricing_plans.items():
            plans[tier.value] = {
                'name': plan.name,
                'description': plan.description,
                'monthly_price': plan.monthly_price / 100,  # Convert to dollars
                'annual_price': plan.annual_price / 100,
                'features': plan.features,
                'savings': round((plan.monthly_price * 12 - plan.annual_price) / 100, 2)
            }
        return plans
    
    def create_checkout_session(self, user_id: str, tier: SubscriptionTier, 
                              billing_period: str = 'monthly') -> Dict[str, Any]:
        """Create Stripe checkout session for subscription"""
        try:
            plan = self.pricing_plans[tier]
            price_id = (plan.stripe_price_id_monthly if billing_period == 'monthly' 
                       else plan.stripe_price_id_annual)
            
            # Create Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:8000')}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:8000')}/payment-cancelled",
                client_reference_id=user_id,
                metadata={
                    'user_id': user_id,
                    'tier': tier.value,
                    'billing_period': billing_period
                }
            )
            
            # Record payment attempt
            payment_record = PaymentRecord(
                payment_id=session.id,
                user_id=user_id,
                amount=plan.monthly_price if billing_period == 'monthly' else plan.annual_price,
                currency='usd',
                status=PaymentStatus.PENDING,
                tier=tier,
                billing_period=billing_period,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                stripe_payment_intent_id=session.payment_intent
            )
            
            self.payment_records[session.id] = payment_record
            
            return {
                'success': True,
                'checkout_url': session.url,
                'session_id': session.id
            }
            
        except Exception as e:
            current_app.logger.error(f"Error creating checkout session: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_webhook(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        try:
            event_type = event_data.get('type')
            
            if event_type == 'checkout.session.completed':
                session = event_data['data']['object']
                self._handle_successful_payment(session)
                
            elif event_type == 'invoice.payment_succeeded':
                invoice = event_data['data']['object']
                self._handle_subscription_renewal(invoice)
                
            elif event_type == 'invoice.payment_failed':
                invoice = event_data['data']['object']
                self._handle_payment_failure(invoice)
                
            elif event_type == 'customer.subscription.deleted':
                subscription = event_data['data']['object']
                self._handle_subscription_cancellation(subscription)
            
            return {'success': True}
            
        except Exception as e:
            current_app.logger.error(f"Error handling webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_successful_payment(self, session: Dict[str, Any]):
        """Handle successful payment completion"""
        session_id = session['id']
        user_id = session['metadata']['user_id']
        tier = SubscriptionTier(session['metadata']['tier'])
        
        # Update payment record
        if session_id in self.payment_records:
            self.payment_records[session_id].status = PaymentStatus.COMPLETED
            self.payment_records[session_id].updated_at = datetime.now()
            self.payment_records[session_id].stripe_subscription_id = session.get('subscription')
        
        # Update user tier (in production, this would update the database)
        current_app.logger.info(f"User {user_id} upgraded to {tier.value}")
        
        # Send notification (integrate with notification system)
        # notification_system.send_notification(...)
    
    def _handle_subscription_renewal(self, invoice: Dict[str, Any]):
        """Handle subscription renewal"""
        customer_id = invoice['customer']
        subscription_id = invoice['subscription']
        
        current_app.logger.info(f"Subscription {subscription_id} renewed for customer {customer_id}")
    
    def _handle_payment_failure(self, invoice: Dict[str, Any]):
        """Handle payment failure"""
        customer_id = invoice['customer']
        subscription_id = invoice['subscription']
        
        current_app.logger.warning(f"Payment failed for subscription {subscription_id}, customer {customer_id}")
        
        # Send notification about payment failure
        # notification_system.send_notification(...)
    
    def _handle_subscription_cancellation(self, subscription: Dict[str, Any]):
        """Handle subscription cancellation"""
        subscription_id = subscription['id']
        customer_id = subscription['customer']
        
        current_app.logger.info(f"Subscription {subscription_id} cancelled for customer {customer_id}")
        
        # Downgrade user tier (in production, this would update the database)
        # Update to free tier or appropriate downgrade logic
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's current subscription details"""
        # In production, this would query the database
        # For now, return mock data
        return {
            'tier': 'tier_2',
            'status': 'active',
            'current_period_end': (datetime.now() + timedelta(days=30)).isoformat(),
            'cancel_at_period_end': False
        }
    
    def cancel_subscription(self, user_id: str, subscription_id: str) -> Dict[str, Any]:
        """Cancel user subscription"""
        try:
            # Cancel Stripe subscription
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            
            return {
                'success': True,
                'message': 'Subscription will be cancelled at the end of the current billing period'
            }
            
        except Exception as e:
            current_app.logger.error(f"Error cancelling subscription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_payment_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's payment history"""
        user_payments = [
            record for record in self.payment_records.values() 
            if record.user_id == user_id
        ]
        
        return [
            {
                'payment_id': record.payment_id,
                'amount': record.amount / 100,  # Convert to dollars
                'currency': record.currency,
                'status': record.status.value,
                'tier': record.tier.value,
                'billing_period': record.billing_period,
                'created_at': record.created_at.isoformat(),
                'updated_at': record.updated_at.isoformat()
            }
            for record in user_payments
        ]

# Global payment integration instance
payment_integration = PaymentIntegration()

def get_payment_integration():
    """Get the global payment integration instance"""
    return payment_integration

