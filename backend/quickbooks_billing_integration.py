"""
QuickBooks Billing Integration System for OBJX Intelligence Platform
Automatically connects project expenses, invoicing, and financial tracking
Aligned with Trinity Foundation methodology: clarify • compound • create
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from decimal import Decimal
import re

class QuickBooksBillingIntegrationManager:
    """
    Manages QuickBooks integration for automatic project billing and expense tracking
    Uses agent intelligence to organize financial data and automate invoicing
    """
    
    def __init__(self):
        self.expense_categories = {
            'permits': {
                'name': 'Permits & Fees',
                'qb_account': 'Professional Fees',
                'tax_deductible': True,
                'project_phase': 'clarify'
            },
            'materials': {
                'name': 'Construction Materials',
                'qb_account': 'Materials & Supplies',
                'tax_deductible': True,
                'project_phase': 'create'
            },
            'labor': {
                'name': 'Labor & Contractors',
                'qb_account': 'Contractor Payments',
                'tax_deductible': True,
                'project_phase': 'complete'
            },
            'professional_services': {
                'name': 'Professional Services',
                'qb_account': 'Professional Fees',
                'tax_deductible': True,
                'project_phase': 'compound'
            },
            'utilities': {
                'name': 'Utilities & Services',
                'qb_account': 'Utilities',
                'tax_deductible': True,
                'project_phase': 'complete'
            },
            'equipment': {
                'name': 'Equipment & Tools',
                'qb_account': 'Equipment',
                'tax_deductible': True,
                'project_phase': 'create'
            },
            'travel': {
                'name': 'Travel & Transportation',
                'qb_account': 'Travel',
                'tax_deductible': True,
                'project_phase': 'complete'
            },
            'office': {
                'name': 'Office & Administrative',
                'qb_account': 'Office Expenses',
                'tax_deductible': True,
                'project_phase': 'clarify'
            }
        }
        
        self.invoice_templates = {
            'permit_application': {
                'name': 'Permit Application Services',
                'description': 'Professional services for permit application and municipal review',
                'default_rate': 150.00,
                'billing_unit': 'hour',
                'trinity_phase': 'clarify'
            },
            'design_review': {
                'name': 'Design Review & Analysis',
                'description': 'Architectural and engineering design review services',
                'default_rate': 175.00,
                'billing_unit': 'hour',
                'trinity_phase': 'compound'
            },
            'project_management': {
                'name': 'Project Management Services',
                'description': 'Comprehensive project coordination and management',
                'default_rate': 125.00,
                'billing_unit': 'hour',
                'trinity_phase': 'create'
            },
            'compliance_review': {
                'name': 'Code Compliance Review',
                'description': 'Building code and regulatory compliance analysis',
                'default_rate': 160.00,
                'billing_unit': 'hour',
                'trinity_phase': 'complete'
            },
            'consultation': {
                'name': 'Strategic Consultation',
                'description': 'Strategic planning and advisory services',
                'default_rate': 200.00,
                'billing_unit': 'hour',
                'trinity_phase': 'compound'
            }
        }
        
        self.payment_terms = {
            'net_15': {'days': 15, 'description': 'Net 15 days'},
            'net_30': {'days': 30, 'description': 'Net 30 days'},
            'due_on_receipt': {'days': 0, 'description': 'Due upon receipt'},
            'net_45': {'days': 45, 'description': 'Net 45 days'}
        }
    
    def analyze_project_expenses(self, project_data: Dict[str, Any], expense_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze project expenses and categorize them for QuickBooks integration
        Uses Trinity Foundation methodology to organize financial data
        """
        try:
            analysis_result = {
                'total_expenses': Decimal('0.00'),
                'categorized_expenses': {},
                'trinity_distribution': {'clarify': 0, 'compound': 0, 'create': 0, 'complete': 0},
                'qb_integration_suggestions': [],
                'tax_implications': {},
                'budget_analysis': {},
                'automation_opportunities': []
            }
            
            # Initialize expense categories
            for category in self.expense_categories:
                analysis_result['categorized_expenses'][category] = {
                    'total': Decimal('0.00'),
                    'items': [],
                    'qb_account': self.expense_categories[category]['qb_account'],
                    'trinity_phase': self.expense_categories[category]['project_phase']
                }
            
            # Analyze each expense
            for expense in expense_data:
                categorized_expense = self._categorize_expense(expense)
                category = categorized_expense['category']
                amount = Decimal(str(expense.get('amount', 0)))
                
                # Add to category total
                analysis_result['categorized_expenses'][category]['total'] += amount
                analysis_result['categorized_expenses'][category]['items'].append(categorized_expense)
                
                # Add to total expenses
                analysis_result['total_expenses'] += amount
                
                # Add to Trinity distribution
                trinity_phase = self.expense_categories[category]['project_phase']
                analysis_result['trinity_distribution'][trinity_phase] += float(amount)
            
            # Generate QuickBooks integration suggestions
            analysis_result['qb_integration_suggestions'] = self._generate_qb_integration_suggestions(
                analysis_result['categorized_expenses']
            )
            
            # Analyze tax implications
            analysis_result['tax_implications'] = self._analyze_tax_implications(
                analysis_result['categorized_expenses']
            )
            
            # Budget analysis
            project_budget = Decimal(str(project_data.get('budget', 0)))
            analysis_result['budget_analysis'] = self._analyze_budget_performance(
                analysis_result['total_expenses'], project_budget, analysis_result['categorized_expenses']
            )
            
            # Generate automation opportunities
            analysis_result['automation_opportunities'] = self._generate_expense_automation_opportunities(
                expense_data, analysis_result['categorized_expenses']
            )
            
            return {
                'success': True,
                'analysis': analysis_result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to analyze project expenses: {str(e)}"
            }
    
    def connect_quickbooks(self, company_id: str, access_token: str, refresh_token: str) -> Dict[str, Any]:
        """
        Establish connection to QuickBooks Online API
        """
        try:
            # Store connection credentials (in production, use secure storage)
            connection_data = {
                'company_id': company_id,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'connected_at': datetime.now().isoformat(),
                'status': 'connected'
            }
            
            # Test connection by fetching company info
            company_info = self._test_quickbooks_connection(connection_data)
            
            return {
                'success': True,
                'connection': connection_data,
                'company_info': company_info,
                'message': 'Successfully connected to QuickBooks Online'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to connect to QuickBooks: {str(e)}"
            }
    
    def categorize_project_expense(self, project_id: str, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically categorize and sync project expense with QuickBooks
        """
        try:
            # Analyze expense using Trinity Foundation methodology
            categorized_expense = self._categorize_expense(expense_data)
            
            # Generate QuickBooks entry
            qb_expense = self._create_quickbooks_expense_entry(
                project_id, categorized_expense
            )
            
            # Generate automation suggestions
            automation_suggestions = self._generate_expense_automation_suggestions(
                categorized_expense
            )
            
            return {
                'success': True,
                'categorized_expense': categorized_expense,
                'quickbooks_entry': qb_expense,
                'automation_suggestions': automation_suggestions,
                'trinity_insights': self._generate_trinity_expense_insights(categorized_expense)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to categorize expense: {str(e)}"
            }
    
    def generate_project_invoice(self, project_id: str, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate invoice for project services using QuickBooks integration
        """
        try:
            invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
            
            # Extract billing information
            client_info = invoice_data.get('client', {})
            services = invoice_data.get('services', [])
            
            # Categorize services by Trinity Foundation phases
            trinity_services = self._categorize_services_by_trinity(services)
            
            # Calculate invoice totals
            invoice_totals = self._calculate_invoice_totals(trinity_services)
            
            # Generate QuickBooks invoice structure
            qb_invoice = self._create_quickbooks_invoice(
                invoice_id, client_info, trinity_services, invoice_totals
            )
            
            # Generate payment automation suggestions
            payment_automation = self._generate_payment_automation_suggestions(
                invoice_data, invoice_totals
            )
            
            return {
                'success': True,
                'invoice': {
                    'id': invoice_id,
                    'client': client_info,
                    'services': trinity_services,
                    'totals': invoice_totals,
                    'quickbooks_data': qb_invoice
                },
                'payment_automation': payment_automation,
                'trinity_insights': self._generate_trinity_invoice_insights(trinity_services)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to generate invoice: {str(e)}"
            }
    
    def get_project_financial_intelligence(self, project_id: str) -> Dict[str, Any]:
        """
        Get comprehensive financial intelligence for a project
        """
        try:
            # Gather financial data from various sources
            financial_data = self._gather_project_financial_data(project_id)
            
            # Analyze using Trinity Foundation methodology
            trinity_analysis = self._analyze_financial_data_by_trinity(financial_data)
            
            # Generate intelligence insights
            intelligence_insights = self._generate_financial_intelligence_insights(
                financial_data, trinity_analysis
            )
            
            # Calculate key financial metrics
            financial_metrics = self._calculate_project_financial_metrics(financial_data)
            
            # Generate optimization recommendations
            optimization_recommendations = self._generate_financial_optimization_recommendations(
                financial_data, trinity_analysis, financial_metrics
            )
            
            return {
                'success': True,
                'financial_intelligence': {
                    'project_id': project_id,
                    'financial_data': financial_data,
                    'trinity_analysis': trinity_analysis,
                    'intelligence_insights': intelligence_insights,
                    'financial_metrics': financial_metrics,
                    'optimization_recommendations': optimization_recommendations,
                    'generated_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to get financial intelligence: {str(e)}"
            }
    
    def setup_billing_automation(self, automation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Setup automated billing rules and workflows
        """
        try:
            automation_rules = []
            
            # Process each automation rule
            for rule_config in automation_config.get('rules', []):
                automation_rule = self._create_automation_rule(rule_config)
                automation_rules.append(automation_rule)
            
            # Setup QuickBooks webhooks for real-time updates
            webhook_config = self._setup_quickbooks_webhooks(automation_config)
            
            # Generate automation monitoring dashboard
            monitoring_config = self._create_automation_monitoring_config(automation_rules)
            
            return {
                'success': True,
                'automation_setup': {
                    'rules': automation_rules,
                    'webhooks': webhook_config,
                    'monitoring': monitoring_config,
                    'trinity_alignment': self._analyze_automation_trinity_alignment(automation_rules)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to setup billing automation: {str(e)}"
            }

    def generate_project_invoice(self, project_data: Dict[str, Any], billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate invoice for project services using QuickBooks integration
        """
        try:
            invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
            
            # Extract billing information
            client_info = billing_data.get('client', {})
            services = billing_data.get('services', [])
            billing_period = billing_data.get('period', {})
            
            # Calculate invoice totals
            invoice_data = {
                'invoice_id': invoice_id,
                'project_id': project_data.get('id', ''),
                'client': client_info,
                'invoice_date': datetime.now().isoformat(),
                'due_date': self._calculate_due_date(billing_data.get('payment_terms', 'net_30')),
                'line_items': [],
                'subtotal': Decimal('0.00'),
                'tax_rate': Decimal(str(billing_data.get('tax_rate', 0))),
                'tax_amount': Decimal('0.00'),
                'total_amount': Decimal('0.00'),
                'trinity_breakdown': {'clarify': 0, 'compound': 0, 'create': 0, 'complete': 0},
                'qb_integration': {},
                'payment_terms': billing_data.get('payment_terms', 'net_30')
            }
            
            # Process each service/line item
            for service in services:
                line_item = self._create_invoice_line_item(service)
                invoice_data['line_items'].append(line_item)
                invoice_data['subtotal'] += line_item['total']
                
                # Add to Trinity breakdown
                trinity_phase = line_item.get('trinity_phase', 'clarify')
                invoice_data['trinity_breakdown'][trinity_phase] += float(line_item['total'])\n            \n            # Calculate tax and total\n            invoice_data['tax_amount'] = invoice_data['subtotal'] * (invoice_data['tax_rate'] / 100)\n            invoice_data['total_amount'] = invoice_data['subtotal'] + invoice_data['tax_amount']\n            \n            # Generate QuickBooks integration data\n            invoice_data['qb_integration'] = self._generate_qb_invoice_data(invoice_data)\n            \n            # Generate payment tracking\n            invoice_data['payment_tracking'] = self._setup_payment_tracking(invoice_data)\n            \n            return {\n                'success': True,\n                'invoice': invoice_data,\n                'qb_sync_instructions': self._generate_qb_sync_instructions(invoice_data)\n            }\n            \n        except Exception as e:\n            return {\n                'success': False,\n                'error': f\"Failed to generate invoice: {str(e)}\"\n            }\n    \n    def _categorize_expense(self, expense: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"\n        Categorize expense based on description and amount\n        \"\"\"\n        description = expense.get('description', '').lower()\n        vendor = expense.get('vendor', '').lower()\n        amount = expense.get('amount', 0)\n        \n        # Keyword-based categorization\n        category = 'office'  # Default category\n        \n        if any(keyword in description for keyword in ['permit', 'fee', 'application', 'license']):\n            category = 'permits'\n        elif any(keyword in description for keyword in ['material', 'supply', 'lumber', 'concrete', 'steel']):\n            category = 'materials'\n        elif any(keyword in description for keyword in ['labor', 'contractor', 'worker', 'crew']):\n            category = 'labor'\n        elif any(keyword in description for keyword in ['architect', 'engineer', 'consultant', 'professional']):\n            category = 'professional_services'\n        elif any(keyword in description for keyword in ['electric', 'water', 'gas', 'utility']):\n            category = 'utilities'\n        elif any(keyword in description for keyword in ['equipment', 'tool', 'machinery', 'rental']):\n            category = 'equipment'\n        elif any(keyword in description for keyword in ['travel', 'mileage', 'fuel', 'transportation']):\n            category = 'travel'\n        \n        return {\n            'id': expense.get('id', ''),\n            'description': expense.get('description', ''),\n            'vendor': expense.get('vendor', ''),\n            'amount': amount,\n            'date': expense.get('date', ''),\n            'category': category,\n            'qb_account': self.expense_categories[category]['qb_account'],\n            'trinity_phase': self.expense_categories[category]['project_phase'],\n            'tax_deductible': self.expense_categories[category]['tax_deductible'],\n            'confidence': self._calculate_categorization_confidence(description, category)\n        }\n    \n    def _calculate_categorization_confidence(self, description: str, category: str) -> float:\n        \"\"\"\n        Calculate confidence level for expense categorization\n        \"\"\"\n        # Simple keyword matching confidence\n        category_keywords = {\n            'permits': ['permit', 'fee', 'application', 'license'],\n            'materials': ['material', 'supply', 'lumber', 'concrete'],\n            'labor': ['labor', 'contractor', 'worker'],\n            'professional_services': ['architect', 'engineer', 'consultant'],\n            'utilities': ['electric', 'water', 'gas', 'utility'],\n            'equipment': ['equipment', 'tool', 'machinery'],\n            'travel': ['travel', 'mileage', 'fuel'],\n            'office': ['office', 'admin', 'supplies']\n        }\n        \n        keywords = category_keywords.get(category, [])\n        matches = sum(1 for keyword in keywords if keyword in description.lower())\n        \n        if matches >= 2:\n            return 0.95\n        elif matches == 1:\n            return 0.80\n        else:\n            return 0.60\n    \n    def _generate_qb_integration_suggestions(self, categorized_expenses: Dict) -> List[Dict[str, Any]]:\n        \"\"\"\n        Generate suggestions for QuickBooks integration\n        \"\"\"\n        suggestions = []\n        \n        # Account mapping suggestions\n        for category, data in categorized_expenses.items():\n            if data['total'] > 0:\n                suggestions.append({\n                    'type': 'account_mapping',\n                    'category': category,\n                    'qb_account': data['qb_account'],\n                    'amount': float(data['total']),\n                    'description': f\"Map {category} expenses to {data['qb_account']} account\",\n                    'priority': 'high' if data['total'] > 1000 else 'medium'\n                })\n        \n        # Automation suggestions\n        suggestions.append({\n            'type': 'automation',\n            'description': 'Set up automatic expense categorization rules',\n            'benefits': ['Reduced manual work', 'Improved accuracy', 'Real-time updates'],\n            'setup_steps': [\n                'Create expense categorization rules',\n                'Set up automatic QB sync',\n                'Configure approval workflows'\n            ]\n        })\n        \n        # Reporting suggestions\n        suggestions.append({\n            'type': 'reporting',\n            'description': 'Create project-specific financial reports',\n            'benefits': ['Better project profitability tracking', 'Improved budgeting', 'Tax preparation'],\n            'setup_steps': [\n                'Create custom report templates',\n                'Set up automated report generation',\n                'Configure stakeholder distribution'\n            ]\n        })\n        \n        return suggestions\n    \n    def _analyze_tax_implications(self, categorized_expenses: Dict) -> Dict[str, Any]:\n        \"\"\"\n        Analyze tax implications of project expenses\n        \"\"\"\n        tax_analysis = {\n            'total_deductible': Decimal('0.00'),\n            'total_non_deductible': Decimal('0.00'),\n            'deductible_by_category': {},\n            'tax_savings_estimate': Decimal('0.00'),\n            'recommendations': []\n        }\n        \n        # Calculate deductible amounts\n        for category, data in categorized_expenses.items():\n            is_deductible = self.expense_categories[category]['tax_deductible']\n            amount = data['total']\n            \n            if is_deductible:\n                tax_analysis['total_deductible'] += amount\n                tax_analysis['deductible_by_category'][category] = float(amount)\n            else:\n                tax_analysis['total_non_deductible'] += amount\n        \n        # Estimate tax savings (assuming 25% tax rate)\n        tax_analysis['tax_savings_estimate'] = tax_analysis['total_deductible'] * Decimal('0.25')\n        \n        # Generate recommendations\n        if tax_analysis['total_deductible'] > 5000:\n            tax_analysis['recommendations'].append({\n                'type': 'documentation',\n                'description': 'Ensure proper documentation for large deductible expenses',\n                'priority': 'high'\n            })\n        \n        tax_analysis['recommendations'].append({\n            'type': 'quarterly_review',\n            'description': 'Schedule quarterly tax review with accountant',\n            'priority': 'medium'\n        })\n        \n        return tax_analysis\n    \n    def _analyze_budget_performance(self, total_expenses: Decimal, project_budget: Decimal, categorized_expenses: Dict) -> Dict[str, Any]:\n        \"\"\"\n        Analyze budget performance and variance\n        \"\"\"\n        budget_analysis = {\n            'budget_utilization': 0.0,\n            'remaining_budget': Decimal('0.00'),\n            'variance': Decimal('0.00'),\n            'variance_percentage': 0.0,\n            'status': 'on_track',\n            'category_performance': {},\n            'recommendations': []\n        }\n        \n        if project_budget > 0:\n            budget_analysis['budget_utilization'] = float(total_expenses / project_budget * 100)\n            budget_analysis['remaining_budget'] = project_budget - total_expenses\n            budget_analysis['variance'] = total_expenses - project_budget\n            budget_analysis['variance_percentage'] = float(budget_analysis['variance'] / project_budget * 100)\n            \n            # Determine status\n            if budget_analysis['budget_utilization'] > 110:\n                budget_analysis['status'] = 'over_budget'\n            elif budget_analysis['budget_utilization'] > 90:\n                budget_analysis['status'] = 'at_risk'\n            elif budget_analysis['budget_utilization'] < 50:\n                budget_analysis['status'] = 'under_utilized'\n            else:\n                budget_analysis['status'] = 'on_track'\n        \n        # Category performance analysis\n        for category, data in categorized_expenses.items():\n            if data['total'] > 0:\n                budget_analysis['category_performance'][category] = {\n                    'amount': float(data['total']),\n                    'percentage_of_total': float(data['total'] / total_expenses * 100) if total_expenses > 0 else 0\n                }\n        \n        # Generate recommendations\n        if budget_analysis['status'] == 'over_budget':\n            budget_analysis['recommendations'].append({\n                'type': 'cost_control',\n                'description': 'Implement immediate cost control measures',\n                'priority': 'critical'\n            })\n        elif budget_analysis['status'] == 'at_risk':\n            budget_analysis['recommendations'].append({\n                'type': 'monitoring',\n                'description': 'Increase budget monitoring frequency',\n                'priority': 'high'\n            })\n        \n        return budget_analysis\n    \n    def _generate_expense_automation_opportunities(self, expense_data: List, categorized_expenses: Dict) -> List[Dict[str, Any]]:\n        \"\"\"\n        Generate automation opportunities for expense management\n        \"\"\"\n        opportunities = []\n        \n        # Receipt scanning automation\n        opportunities.append({\n            'type': 'receipt_scanning',\n            'description': 'Automatically scan and categorize receipts',\n            'confidence': 0.85,\n            'setup_steps': [\n                'Set up receipt scanning app integration',\n                'Configure automatic categorization rules',\n                'Enable QuickBooks sync'\n            ],\n            'benefits': ['Reduced manual entry', 'Improved accuracy', 'Real-time expense tracking']\n        })\n        \n        # Vendor payment automation\n        if any(cat['total'] > 1000 for cat in categorized_expenses.values()):\n            opportunities.append({\n                'type': 'vendor_payment_automation',\n                'description': 'Set up automatic vendor payment processing',\n                'confidence': 0.80,\n                'setup_steps': [\n                    'Configure vendor payment terms',\n                    'Set up approval workflows',\n                    'Enable automatic payment scheduling'\n                ],\n                'benefits': ['Improved cash flow', 'Better vendor relationships', 'Reduced late fees']\n            })\n        \n        # Budget alert automation\n        opportunities.append({\n            'type': 'budget_alerts',\n            'description': 'Automatically monitor budget thresholds and send alerts',\n            'confidence': 0.90,\n            'setup_steps': [\n                'Set budget threshold alerts',\n                'Configure notification recipients',\n                'Enable real-time monitoring'\n            ],\n            'benefits': ['Proactive budget management', 'Prevent cost overruns', 'Improved financial control']\n        })\n        \n        return opportunities\n    \n    def _calculate_due_date(self, payment_terms: str) -> str:\n        \"\"\"\n        Calculate invoice due date based on payment terms\n        \"\"\"\n        terms = self.payment_terms.get(payment_terms, self.payment_terms['net_30'])\n        due_date = datetime.now() + timedelta(days=terms['days'])\n        return due_date.isoformat()\n    \n    def _create_invoice_line_item(self, service: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"\n        Create invoice line item from service data\n        \"\"\"\n        service_type = service.get('type', 'consultation')\n        template = self.invoice_templates.get(service_type, self.invoice_templates['consultation'])\n        \n        quantity = Decimal(str(service.get('quantity', 1)))\n        rate = Decimal(str(service.get('rate', template['default_rate'])))\n        total = quantity * rate\n        \n        return {\n            'service_type': service_type,\n            'description': service.get('description', template['description']),\n            'quantity': float(quantity),\n            'rate': float(rate),\n            'total': total,\n            'billing_unit': template['billing_unit'],\n            'trinity_phase': template['trinity_phase'],\n            'date_range': service.get('date_range', ''),\n            'notes': service.get('notes', '')\n        }\n    \n    def _generate_qb_invoice_data(self, invoice_data: Dict) -> Dict[str, Any]:\n        \"\"\"\n        Generate QuickBooks-specific invoice data\n        \"\"\"\n        return {\n            'customer_ref': {\n                'name': invoice_data['client'].get('name', ''),\n                'email': invoice_data['client'].get('email', '')\n            },\n            'invoice_number': invoice_data['invoice_id'],\n            'txn_date': invoice_data['invoice_date'][:10],  # YYYY-MM-DD format\n            'due_date': invoice_data['due_date'][:10],\n            'line_items': [\n                {\n                    'description': item['description'],\n                    'quantity': item['quantity'],\n                    'unit_price': item['rate'],\n                    'amount': float(item['total'])\n                }\n                for item in invoice_data['line_items']\n            ],\n            'subtotal': float(invoice_data['subtotal']),\n            'tax_rate': float(invoice_data['tax_rate']),\n            'tax_amount': float(invoice_data['tax_amount']),\n            'total_amount': float(invoice_data['total_amount']),\n            'payment_terms': invoice_data['payment_terms']\n        }\n    \n    def _setup_payment_tracking(self, invoice_data: Dict) -> Dict[str, Any]:\n        \"\"\"\n        Set up payment tracking for invoice\n        \"\"\"\n        return {\n            'status': 'sent',\n            'amount_due': float(invoice_data['total_amount']),\n            'amount_paid': 0.0,\n            'payment_history': [],\n            'reminder_schedule': [\n                {\n                    'days_after_due': 7,\n                    'type': 'gentle_reminder',\n                    'sent': False\n                },\n                {\n                    'days_after_due': 14,\n                    'type': 'firm_reminder',\n                    'sent': False\n                },\n                {\n                    'days_after_due': 30,\n                    'type': 'final_notice',\n                    'sent': False\n                }\n            ],\n            'late_fee_policy': {\n                'enabled': True,\n                'rate': 1.5,  # 1.5% per month\n                'grace_period_days': 10\n            }\n        }\n    \n    def _generate_qb_sync_instructions(self, invoice_data: Dict) -> List[Dict[str, Any]]:\n        \"\"\"\n        Generate step-by-step QuickBooks sync instructions\n        \"\"\"\n        return [\n            {\n                'step': 1,\n                'action': 'Create Customer',\n                'description': f\"Create customer record for {invoice_data['client'].get('name', 'Unknown')}\",\n                'qb_location': 'Sales > Customers',\n                'data_required': ['Customer name', 'Email', 'Billing address']\n            },\n            {\n                'step': 2,\n                'action': 'Create Invoice',\n                'description': f\"Create invoice {invoice_data['invoice_id']}\",\n                'qb_location': 'Sales > Invoices',\n                'data_required': ['Customer', 'Invoice date', 'Due date', 'Line items']\n            },\n            {\n                'step': 3,\n                'action': 'Set Payment Terms',\n                'description': f\"Set payment terms to {invoice_data['payment_terms']}\",\n                'qb_location': 'Invoice > Payment Terms',\n                'data_required': ['Payment terms']\n            },\n            {\n                'step': 4,\n                'action': 'Send Invoice',\n                'description': 'Send invoice to customer via email',\n                'qb_location': 'Invoice > Send',\n                'data_required': ['Customer email']\n            },\n            {\n                'step': 5,\n                'action': 'Set Up Payment Tracking',\n                'description': 'Enable automatic payment reminders',\n                'qb_location': 'Settings > Payment Reminders',\n                'data_required': ['Reminder schedule']\n            }\n        ]\n\n# Initialize the QuickBooks billing integration manager\nquickbooks_manager = QuickBooksBillingIntegrationManager()"

