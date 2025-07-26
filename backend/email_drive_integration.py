"""
Email and Google Drive Integration System for OBJX Intelligence Platform
Automatically connects emails, drive files, and project data
Aligned with Trinity Foundation methodology: clarify • compound • create
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

class EmailDriveIntegrationManager:
    """
    Manages email and Google Drive integration with automatic project organization
    Uses agent intelligence to understand connections and organize data
    """
    
    def __init__(self):
        self.email_patterns = {
            'project_keywords': ['project', 'permit', 'application', 'review', 'approval', 'construction', 'renovation', 'adu'],
            'client_indicators': ['client', 'customer', 'property owner', 'applicant'],
            'deadline_patterns': [
                r'due\s+(?:by\s+)?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'deadline\s+(?:is\s+)?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'by\s+(\w+\s+\d{1,2},?\s+\d{4})',
                r'before\s+(\w+\s+\d{1,2},?\s+\d{4})'
            ],
            'cost_patterns': [
                r'\$[\d,]+\.?\d*',
                r'cost[:\s]+\$?[\d,]+\.?\d*',
                r'budget[:\s]+\$?[\d,]+\.?\d*',
                r'fee[:\s]+\$?[\d,]+\.?\d*'
            ],
            'address_patterns': [
                r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Road|Rd|Way|Circle|Cir|Court|Ct)',
                r'\d+\s+[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}'
            ]
        }
        
        self.drive_file_categories = {
            'permits': ['permit', 'application', 'approval', 'license'],
            'plans': ['plan', 'drawing', 'blueprint', 'design', 'layout'],
            'reports': ['report', 'analysis', 'study', 'assessment', 'review'],
            'contracts': ['contract', 'agreement', 'proposal', 'estimate'],
            'correspondence': ['email', 'letter', 'communication', 'memo'],
            'photos': ['photo', 'image', 'picture', 'site', 'progress'],
            'invoices': ['invoice', 'bill', 'receipt', 'payment', 'cost'],
            'compliance': ['compliance', 'code', 'regulation', 'requirement', 'standard']
        }
    
    def analyze_email_for_project_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email content to extract project-relevant information
        Uses Trinity Foundation methodology to categorize findings
        """
        try:
            subject = email_data.get('subject', '')
            body = email_data.get('body', '')
            sender = email_data.get('sender', '')
            recipients = email_data.get('recipients', [])
            date = email_data.get('date', '')
            
            # Combine all text for analysis
            full_text = f"{subject} {body}".lower()
            
            # Extract project information
            extracted_data = {
                'project_relevance': self._calculate_project_relevance(full_text),
                'extracted_fields': [],
                'suggested_connections': [],
                'trinity_categorization': {},
                'automation_opportunities': []
            }
            
            # Extract addresses
            addresses = self._extract_addresses(full_text)
            for address in addresses:
                extracted_data['extracted_fields'].append({
                    'name': 'Project Address',
                    'type': 'address',
                    'value': address,
                    'confidence': 0.85,
                    'trinity_category': 'clarify',
                    'source': 'email_analysis'
                })
            
            # Extract costs/budgets
            costs = self._extract_costs(full_text)
            for cost in costs:
                extracted_data['extracted_fields'].append({
                    'name': 'Project Cost',
                    'type': 'currency',
                    'value': cost,
                    'confidence': 0.80,
                    'trinity_category': 'clarify',
                    'source': 'email_analysis'
                })
            
            # Extract deadlines
            deadlines = self._extract_deadlines(full_text)
            for deadline in deadlines:
                extracted_data['extracted_fields'].append({
                    'name': 'Project Deadline',
                    'type': 'date',
                    'value': deadline,
                    'confidence': 0.90,
                    'trinity_category': 'complete',
                    'source': 'email_analysis'
                })
            
            # Extract contacts
            contacts = self._extract_contacts(sender, recipients, body)
            for contact in contacts:
                extracted_data['extracted_fields'].append({
                    'name': 'Project Contact',
                    'type': 'contact',
                    'value': contact,
                    'confidence': 0.75,
                    'trinity_category': 'clarify',
                    'source': 'email_analysis'
                })
            
            # Identify project connections
            extracted_data['suggested_connections'] = self._identify_project_connections(
                addresses, costs, deadlines, subject, body
            )
            
            # Generate automation opportunities
            extracted_data['automation_opportunities'] = self._generate_email_automation_opportunities(
                email_data, extracted_data['extracted_fields']
            )
            
            return {
                'success': True,
                'data': extracted_data,
                'email_metadata': {
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'message_id': email_data.get('message_id', ''),
                    'thread_id': email_data.get('thread_id', '')
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to analyze email: {str(e)}"
            }
    
    def analyze_drive_file_for_project_data(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Google Drive file to extract project-relevant information
        """
        try:
            file_name = file_data.get('name', '')
            file_type = file_data.get('mimeType', '')
            file_content = file_data.get('content', '')
            file_path = file_data.get('path', '')
            
            # Analyze file for project relevance
            extracted_data = {
                'project_relevance': self._calculate_file_project_relevance(file_name, file_type, file_content),
                'file_category': self._categorize_drive_file(file_name, file_type),
                'extracted_fields': [],
                'suggested_connections': [],
                'trinity_categorization': {},
                'automation_opportunities': []
            }
            
            # Extract information based on file type
            if 'pdf' in file_type.lower() or 'document' in file_type.lower():
                # Extract text-based information
                text_data = self._extract_text_from_file(file_content, file_type)
                if text_data:
                    # Extract addresses, costs, dates from document content
                    addresses = self._extract_addresses(text_data.lower())
                    costs = self._extract_costs(text_data.lower())
                    deadlines = self._extract_deadlines(text_data.lower())
                    
                    # Add extracted fields
                    for address in addresses:
                        extracted_data['extracted_fields'].append({
                            'name': 'Document Address',
                            'type': 'address',
                            'value': address,
                            'confidence': 0.85,
                            'trinity_category': 'clarify',
                            'source': 'document_analysis'
                        })
            
            elif 'image' in file_type.lower():
                # For images, analyze filename and metadata
                extracted_data['extracted_fields'].append({
                    'name': 'Project Photo',
                    'type': 'file',
                    'value': file_name,
                    'confidence': 0.70,
                    'trinity_category': 'compound',
                    'source': 'image_analysis'
                })
            
            elif 'spreadsheet' in file_type.lower():
                # For spreadsheets, look for budget/cost information
                extracted_data['extracted_fields'].append({
                    'name': 'Project Budget Spreadsheet',
                    'type': 'file',
                    'value': file_name,
                    'confidence': 0.80,
                    'trinity_category': 'clarify',
                    'source': 'spreadsheet_analysis'
                })
            
            # Generate file organization suggestions
            extracted_data['automation_opportunities'] = self._generate_file_automation_opportunities(
                file_data, extracted_data['file_category']
            )
            
            return {
                'success': True,
                'data': extracted_data,
                'file_metadata': {
                    'name': file_name,
                    'type': file_type,
                    'size': file_data.get('size', 0),
                    'modified': file_data.get('modifiedTime', ''),
                    'drive_id': file_data.get('id', ''),
                    'path': file_path
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to analyze drive file: {str(e)}"
            }
    
    def _calculate_project_relevance(self, text: str) -> float:
        """
        Calculate how relevant an email is to project management
        """
        relevance_score = 0.0
        
        # Check for project keywords
        project_keywords = self.email_patterns['project_keywords']
        keyword_matches = sum(1 for keyword in project_keywords if keyword in text)
        relevance_score += min(keyword_matches * 0.2, 0.6)
        
        # Check for addresses (strong indicator)
        if any(re.search(pattern, text) for pattern in self.email_patterns['address_patterns']):
            relevance_score += 0.3
        
        # Check for costs/budgets
        if any(re.search(pattern, text) for pattern in self.email_patterns['cost_patterns']):
            relevance_score += 0.2
        
        # Check for deadlines
        if any(re.search(pattern, text) for pattern in self.email_patterns['deadline_patterns']):
            relevance_score += 0.2
        
        return min(relevance_score, 1.0)
    
    def _calculate_file_project_relevance(self, file_name: str, file_type: str, content: str) -> float:
        """
        Calculate how relevant a file is to project management
        """
        relevance_score = 0.0
        
        # Analyze filename
        filename_lower = file_name.lower()
        for category, keywords in self.drive_file_categories.items():
            if any(keyword in filename_lower for keyword in keywords):
                relevance_score += 0.3
                break
        
        # Analyze file type
        if any(doc_type in file_type.lower() for doc_type in ['pdf', 'document', 'spreadsheet']):
            relevance_score += 0.2
        elif 'image' in file_type.lower():
            relevance_score += 0.1
        
        # Analyze content if available
        if content:
            content_lower = content.lower()
            project_indicators = ['permit', 'application', 'project', 'construction', 'renovation']
            content_matches = sum(1 for indicator in project_indicators if indicator in content_lower)
            relevance_score += min(content_matches * 0.1, 0.3)
        
        return min(relevance_score, 1.0)
    
    def _extract_addresses(self, text: str) -> List[str]:
        """
        Extract addresses from text using regex patterns
        """
        addresses = []
        for pattern in self.email_patterns['address_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            addresses.extend(matches)
        return list(set(addresses))  # Remove duplicates
    
    def _extract_costs(self, text: str) -> List[str]:
        """
        Extract cost/budget information from text
        """
        costs = []
        for pattern in self.email_patterns['cost_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            costs.extend(matches)
        return list(set(costs))
    
    def _extract_deadlines(self, text: str) -> List[str]:
        """
        Extract deadline information from text
        """
        deadlines = []
        for pattern in self.email_patterns['deadline_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            deadlines.extend(matches)
        return list(set(deadlines))
    
    def _extract_contacts(self, sender: str, recipients: List[str], body: str) -> List[Dict[str, str]]:
        """
        Extract contact information from email
        """
        contacts = []
        
        # Add sender
        if sender:
            contacts.append({
                'email': sender,
                'role': 'sender',
                'type': 'email'
            })
        
        # Add recipients
        for recipient in recipients:
            contacts.append({
                'email': recipient,
                'role': 'recipient',
                'type': 'email'
            })
        
        # Extract phone numbers from body
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, body)
        for phone in phones:
            contacts.append({
                'phone': phone,
                'type': 'phone'
            })
        
        return contacts
    
    def _categorize_drive_file(self, file_name: str, file_type: str) -> str:
        """
        Categorize drive file based on name and type
        """
        filename_lower = file_name.lower()
        
        for category, keywords in self.drive_file_categories.items():
            if any(keyword in filename_lower for keyword in keywords):
                return category
        
        # Fallback based on file type
        if 'image' in file_type.lower():
            return 'photos'
        elif 'spreadsheet' in file_type.lower():
            return 'reports'
        elif 'document' in file_type.lower():
            return 'correspondence'
        
        return 'other'
    
    def _extract_text_from_file(self, content: str, file_type: str) -> str:
        """
        Extract text content from file based on type
        This is a simplified version - in production, you'd use proper libraries
        """
        # For now, return content as-is
        # In production, you'd use libraries like PyPDF2, python-docx, etc.
        return content
    
    def _identify_project_connections(self, addresses: List[str], costs: List[str], deadlines: List[str], subject: str, body: str) -> List[Dict[str, Any]]:
        """
        Identify potential connections to existing projects
        """
        connections = []
        
        # Address-based connections
        for address in addresses:
            connections.append({
                'type': 'address_match',
                'value': address,
                'confidence': 0.90,
                'description': f'Email mentions address: {address}',
                'suggested_action': 'Link to project with matching address'
            })
        
        # Subject-based connections
        if any(keyword in subject.lower() for keyword in ['permit', 'application', 'project']):
            connections.append({
                'type': 'subject_relevance',
                'value': subject,
                'confidence': 0.75,
                'description': 'Email subject indicates project relevance',
                'suggested_action': 'Review for project assignment'
            })
        
        return connections
    
    def _generate_email_automation_opportunities(self, email_data: Dict, extracted_fields: List[Dict]) -> List[Dict[str, Any]]:
        """
        Generate automation opportunities for email integration
        """
        opportunities = []
        
        # Auto-filing opportunity
        if extracted_fields:
            opportunities.append({
                'type': 'auto_filing',
                'description': 'Automatically file email in project folder',
                'confidence': 0.85,
                'setup_steps': [
                    'Create Gmail filter for project emails',
                    'Set up automatic labeling',
                    'Configure project folder sync'
                ],
                'benefits': ['Automatic email organization', 'Improved project tracking', 'Reduced manual work']
            })
        
        # Auto-field population
        if any(field['type'] in ['address', 'currency', 'date'] for field in extracted_fields):
            opportunities.append({
                'type': 'auto_field_population',
                'description': 'Automatically populate project fields from email content',
                'confidence': 0.80,
                'setup_steps': [
                    'Configure field mapping rules',
                    'Set up email parsing automation',
                    'Enable automatic field updates'
                ],
                'benefits': ['Reduced data entry', 'Improved accuracy', 'Real-time updates']
            })
        
        # Deadline tracking
        deadline_fields = [f for f in extracted_fields if f['type'] == 'date']
        if deadline_fields:
            opportunities.append({
                'type': 'deadline_tracking',
                'description': 'Automatically track deadlines mentioned in emails',
                'confidence': 0.90,
                'setup_steps': [
                    'Set up calendar integration',
                    'Configure deadline alerts',
                    'Enable automatic reminders'
                ],
                'benefits': ['Never miss deadlines', 'Proactive project management', 'Automatic scheduling']
            })
        
        return opportunities
    
    def _generate_file_automation_opportunities(self, file_data: Dict, file_category: str) -> List[Dict[str, Any]]:
        """
        Generate automation opportunities for file integration
        """
        opportunities = []
        
        # Auto-organization
        opportunities.append({
            'type': 'auto_organization',
            'description': f'Automatically organize {file_category} files in project folders',
            'confidence': 0.80,
            'setup_steps': [
                'Create project folder structure',
                'Set up file naming conventions',
                'Configure automatic file sorting'
            ],
            'benefits': ['Organized file structure', 'Easy file discovery', 'Consistent organization']
        })
        
        # Version control
        if file_category in ['plans', 'reports', 'contracts']:
            opportunities.append({
                'type': 'version_control',
                'description': 'Automatically track file versions and changes',
                'confidence': 0.75,
                'setup_steps': [
                    'Enable version tracking',
                    'Set up change notifications',
                    'Configure backup system'
                ],
                'benefits': ['Track document changes', 'Prevent version conflicts', 'Maintain history']
            })
        
        # Content extraction
        if file_category in ['permits', 'reports', 'contracts']:
            opportunities.append({
                'type': 'content_extraction',
                'description': 'Automatically extract key information from documents',
                'confidence': 0.70,
                'setup_steps': [
                    'Set up OCR processing',
                    'Configure data extraction rules',
                    'Enable automatic field population'
                ],
                'benefits': ['Automatic data entry', 'Improved accuracy', 'Time savings']
            })
        
        return opportunities
    
    def create_project_integration_plan(self, project_id: str, email_data: List[Dict], file_data: List[Dict]) -> Dict[str, Any]:
        """
        Create a comprehensive integration plan for project emails and files
        """
        try:
            integration_plan = {
                'project_id': project_id,
                'email_integrations': [],
                'file_integrations': [],
                'automation_recommendations': [],
                'setup_priority': [],
                'estimated_time_savings': 0
            }
            
            # Analyze emails
            for email in email_data:
                email_analysis = self.analyze_email_for_project_data(email)
                if email_analysis['success'] and email_analysis['data']['project_relevance'] > 0.5:
                    integration_plan['email_integrations'].append({
                        'email_id': email.get('id', ''),
                        'relevance_score': email_analysis['data']['project_relevance'],
                        'extracted_fields': email_analysis['data']['extracted_fields'],
                        'automation_opportunities': email_analysis['data']['automation_opportunities']
                    })
            
            # Analyze files
            for file in file_data:
                file_analysis = self.analyze_drive_file_for_project_data(file)
                if file_analysis['success'] and file_analysis['data']['project_relevance'] > 0.5:
                    integration_plan['file_integrations'].append({
                        'file_id': file.get('id', ''),
                        'relevance_score': file_analysis['data']['project_relevance'],
                        'file_category': file_analysis['data']['file_category'],
                        'automation_opportunities': file_analysis['data']['automation_opportunities']
                    })
            
            # Generate overall recommendations
            integration_plan['automation_recommendations'] = self._generate_overall_automation_recommendations(
                integration_plan['email_integrations'],
                integration_plan['file_integrations']
            )
            
            # Prioritize setup tasks
            integration_plan['setup_priority'] = self._prioritize_integration_setup(integration_plan)
            
            # Estimate time savings
            integration_plan['estimated_time_savings'] = self._estimate_time_savings(integration_plan)
            
            return {
                'success': True,
                'integration_plan': integration_plan
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to create integration plan: {str(e)}"
            }
    
    def _generate_overall_automation_recommendations(self, email_integrations: List, file_integrations: List) -> List[Dict[str, Any]]:
        """
        Generate overall automation recommendations based on all integrations
        """
        recommendations = []
        
        # Email automation
        if email_integrations:
            recommendations.append({
                'type': 'email_automation',
                'priority': 'high',
                'description': f'Set up automated email processing for {len(email_integrations)} relevant emails',
                'impact': 'high',
                'effort': 'medium'
            })
        
        # File automation
        if file_integrations:
            recommendations.append({
                'type': 'file_automation',
                'priority': 'high',
                'description': f'Set up automated file organization for {len(file_integrations)} relevant files',
                'impact': 'high',
                'effort': 'medium'
            })
        
        # Cross-platform integration
        if email_integrations and file_integrations:
            recommendations.append({
                'type': 'cross_platform_integration',
                'priority': 'medium',
                'description': 'Connect email and file data for comprehensive project tracking',
                'impact': 'very_high',
                'effort': 'high'
            })
        
        return recommendations
    
    def _prioritize_integration_setup(self, integration_plan: Dict) -> List[Dict[str, Any]]:
        """
        Prioritize integration setup tasks based on impact and effort
        """
        tasks = []
        
        # High-impact, low-effort tasks first
        if integration_plan['email_integrations']:
            tasks.append({
                'task': 'Email Auto-Filing Setup',
                'priority': 1,
                'effort': 'low',
                'impact': 'high',
                'estimated_time': '30 minutes'
            })
        
        if integration_plan['file_integrations']:
            tasks.append({
                'task': 'File Organization Setup',
                'priority': 2,
                'effort': 'low',
                'impact': 'high',
                'estimated_time': '45 minutes'
            })
        
        # Medium-impact tasks
        tasks.append({
            'task': 'Automated Field Population',
            'priority': 3,
            'effort': 'medium',
            'impact': 'medium',
            'estimated_time': '2 hours'
        })
        
        # High-impact, high-effort tasks last
        tasks.append({
            'task': 'Cross-Platform Integration',
            'priority': 4,
            'effort': 'high',
            'impact': 'very_high',
            'estimated_time': '4 hours'
        })
        
        return tasks
    
    def _estimate_time_savings(self, integration_plan: Dict) -> int:
        """
        Estimate weekly time savings from automation (in minutes)
        """
        time_savings = 0
        
        # Email automation savings
        email_count = len(integration_plan['email_integrations'])
        time_savings += email_count * 5  # 5 minutes per email for manual filing
        
        # File automation savings
        file_count = len(integration_plan['file_integrations'])
        time_savings += file_count * 3  # 3 minutes per file for manual organization
        
        # Field population savings
        if integration_plan['automation_recommendations']:
            time_savings += 60  # 1 hour per week for automated field population
        
        return time_savings

# Initialize the email and drive integration manager
email_drive_manager = EmailDriveIntegrationManager()

