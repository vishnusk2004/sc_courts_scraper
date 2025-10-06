#!/usr/bin/env python3
"""
SC Courts Scraper Service for Django
"""

import requests
import time
import uuid
import logging
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import ScrapingSession, CourtRecord

logger = logging.getLogger(__name__)

class SCCourtsScraperService:
    def __init__(self):
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def create_session(self):
        """Create a new scraping session"""
        session_id = str(uuid.uuid4())
        session = ScrapingSession.objects.create(
            session_id=session_id,
            status='pending'
        )
        return session
    
    def get_current_ip(self):
        """Get current IP address"""
        try:
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                return response.json().get('origin', '')
        except Exception as e:
            logger.error(f"Error getting IP: {e}")
        return None
    
    def make_initial_request(self, session):
        """Make initial request to establish session"""
        try:
            # First, try to access the main page
            main_url = f"{self.base_url}/dorchester/courtrosters/"
            
            response = requests.get(main_url, headers=self.headers, timeout=30)
            logger.info(f"Initial request status: {response.status_code}")
            
            if response.status_code == 200:
                # Wait a bit before the main request
                time.sleep(2)
                return True
            else:
                logger.warning(f"Initial request failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Initial request error: {e}")
            return False
    
    def scrape_website(self, session):
        """Main scraping function using complete session approach"""
        try:
            # Update session status
            session.status = 'running'
            session.ip_address = self.get_current_ip()
            session.user_agent = self.headers.get('User-Agent', '')
            session.save()
            
            # Use complete session approach
            result = self.run_complete_session()
            
            if result:
                session.status = 'success'
                session.raw_html = result.get('html', '')
                session.parsed_data = result.get('data', {})
                session.forms_count = len(result.get('data', {}).get('forms', []))
                session.inputs_count = len(result.get('data', {}).get('inputs', []))
                session.selects_count = len(result.get('data', {}).get('selects', []))
                session.links_count = len(result.get('data', {}).get('links', []))
                session.scripts_count = len(result.get('data', {}).get('scripts', []))
                session.save()
                return True
            else:
                session.status = 'blocked'
                session.error_message = 'Complete session failed - likely IP blocking'
                session.save()
                return False
                
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            session.status = 'failed'
            session.error_message = str(e)
            session.save()
            return False
    
    def run_complete_session(self):
        """Run the complete session sequence"""
        try:
            # Create session with proper headers
            session = requests.Session()
            session.headers.update(self.headers)
            
            # Make main request
            response = session.get(self.target_url, timeout=30)
            
            if response.status_code == 200:
                if 'Incapsula' in response.text:
                    return False
                else:
                    # Parse successful response
                    parsed_data = self.parse_content(response.text)
                    return {
                        'html': response.text,
                        'data': parsed_data
                    }
            else:
                return False
                
        except Exception as e:
            logger.error(f"Complete session error: {e}")
            return False
    
    def analyze_protection_page(self, html_content):
        """Analyze the protection page to understand what's blocking access"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for common protection indicators
            protection_indicators = {
                'incapsula': 'Incapsula' in html_content,
                'cloudflare': 'Cloudflare' in html_content,
                'ddos_guard': 'DDoS-Guard' in html_content,
                'sucuri': 'Sucuri' in html_content,
                'recaptcha': 'reCAPTCHA' in html_content or 'recaptcha' in html_content.lower(),
                'hcaptcha': 'hCaptcha' in html_content or 'hcaptcha' in html_content.lower(),
                'challenge': 'challenge' in html_content.lower(),
                'verification': 'verification' in html_content.lower(),
                'robot_check': 'robot' in html_content.lower() or 'bot' in html_content.lower(),
                'captcha': 'captcha' in html_content.lower(),
            }
            
            # Look for specific elements
            forms = soup.find_all('form')
            inputs = soup.find_all('input')
            buttons = soup.find_all('button')
            scripts = soup.find_all('script')
            
            # Look for specific protection elements
            protection_elements = {
                'challenge_forms': [form for form in forms if any(keyword in form.get_text().lower() for keyword in ['challenge', 'verify', 'captcha', 'robot'])],
                'captcha_inputs': [input_tag for input_tag in inputs if input_tag.get('type') in ['text', 'hidden'] and any(keyword in str(input_tag).lower() for keyword in ['captcha', 'challenge', 'verify'])],
                'verification_buttons': [button for button in buttons if any(keyword in button.get_text().lower() for keyword in ['verify', 'continue', 'proceed', 'submit'])],
                'protection_scripts': [script for script in scripts if any(keyword in script.get_text().lower() for keyword in ['incapsula', 'cloudflare', 'challenge', 'captcha'])],
            }
            
            # Extract page title and meta information
            title = soup.title.get_text(strip=True) if soup.title else ''
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description.get('content', '') if meta_description else ''
            
            # Look for specific text content
            page_text = soup.get_text()
            protection_texts = {
                'access_denied': 'access denied' in page_text.lower(),
                'blocked': 'blocked' in page_text.lower(),
                'forbidden': 'forbidden' in page_text.lower(),
                'not_authorized': 'not authorized' in page_text.lower(),
                'security_check': 'security check' in page_text.lower(),
                'verification_required': 'verification required' in page_text.lower(),
            }
            
            return {
                'protection_indicators': protection_indicators,
                'protection_elements': protection_elements,
                'protection_texts': protection_texts,
                'page_title': title,
                'meta_description': meta_description,
                'total_forms': len(forms),
                'total_inputs': len(inputs),
                'total_buttons': len(buttons),
                'total_scripts': len(scripts),
                'page_text_preview': page_text[:500] + '...' if len(page_text) > 500 else page_text,
            }
            
        except Exception as e:
            logger.error(f"Error analyzing protection page: {e}")
            return {'error': str(e)}
    
    def parse_content(self, html_content):
        """Parse HTML content and extract useful data"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract forms
            forms = []
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', ''),
                    'id': form.get('id', ''),
                    'class': form.get('class', []),
                    'inputs': []
                }
                
                # Extract form inputs
                for input_tag in form.find_all('input'):
                    input_data = {
                        'type': input_tag.get('type', ''),
                        'name': input_tag.get('name', ''),
                        'value': input_tag.get('value', ''),
                        'id': input_tag.get('id', ''),
                        'class': input_tag.get('class', [])
                    }
                    form_data['inputs'].append(input_data)
                
                forms.append(form_data)
            
            # Extract all inputs
            inputs = []
            for input_tag in soup.find_all('input'):
                input_data = {
                    'type': input_tag.get('type', ''),
                    'name': input_tag.get('name', ''),
                    'value': input_tag.get('value', ''),
                    'id': input_tag.get('id', ''),
                    'class': input_tag.get('class', [])
                }
                inputs.append(input_data)
            
            # Extract select elements
            selects = []
            for select in soup.find_all('select'):
                select_data = {
                    'name': select.get('name', ''),
                    'id': select.get('id', ''),
                    'class': select.get('class', []),
                    'options': []
                }
                
                for option in select.find_all('option'):
                    option_data = {
                        'value': option.get('value', ''),
                        'text': option.get_text(strip=True),
                        'selected': option.get('selected') is not None
                    }
                    select_data['options'].append(option_data)
                
                selects.append(select_data)
            
            # Extract links
            links = []
            for link in soup.find_all('a'):
                link_data = {
                    'href': link.get('href', ''),
                    'text': link.get_text(strip=True),
                    'id': link.get('id', ''),
                    'class': link.get('class', [])
                }
                links.append(link_data)
            
            # Extract scripts
            scripts = []
            for script in soup.find_all('script'):
                script_data = {
                    'src': script.get('src', ''),
                    'type': script.get('type', ''),
                    'content': script.get_text(strip=True)[:500] if script.get_text(strip=True) else ''
                }
                scripts.append(script_data)
            
            return {
                'forms': forms,
                'inputs': inputs,
                'selects': selects,
                'links': links,
                'scripts': scripts,
                'title': soup.title.get_text(strip=True) if soup.title else '',
                'meta_description': soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else ''
            }
            
        except Exception as e:
            logger.error(f"Error parsing content: {e}")
            return {}
    
    def extract_court_records(self, session, parsed_data):
        """Extract court records from parsed data"""
        try:
            # This is a placeholder - you would implement actual record extraction
            # based on the specific structure of the SC courts website
            
            # For now, create a sample record
            if session.forms_count > 0:
                CourtRecord.objects.create(
                    session=session,
                    record_type='Form Data',
                    case_number='N/A',
                    party_name='SC Courts Website',
                    raw_data=parsed_data
                )
                
        except Exception as e:
            logger.error(f"Error extracting court records: {e}")
    
    def run_scraping(self):
        """Run the complete scraping process"""
        session = self.create_session()
        
        try:
            success = self.scrape_website(session)
            return session, success
        except Exception as e:
            logger.error(f"Scraping process error: {e}")
            session.status = 'failed'
            session.error_message = str(e)
            session.save()
            return session, False
