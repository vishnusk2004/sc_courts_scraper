#!/usr/bin/env python3
"""
Enhanced SC Courts Scraper to handle Incapsula protection
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import logging
import random
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SCCourtsScraperEnhanced:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
        # Enhanced headers to bypass protection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Priority': 'u=0, i',
            'Referer': 'https://publicindex.sccourts.org/dorchester/courtrosters/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        self.session.headers.update(self.headers)
        self.delay = 3  # Increased delay
    
    def handle_incapsula_protection(self, response):
        """
        Handle Incapsula protection page
        """
        if 'Incapsula' in response.text or 'SWJIYLWA' in response.text:
            logger.info("Detected Incapsula protection page")
            
            # Try to extract and execute the protection script
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', src=re.compile(r'_Incapsula_Resource'))
            
            if script_tag:
                script_url = script_tag.get('src')
                if script_url:
                    full_script_url = urljoin(self.base_url, script_url)
                    logger.info(f"Found Incapsula script: {full_script_url}")
                    
                    # Try to fetch the script
                    try:
                        script_response = self.session.get(full_script_url)
                        if script_response.status_code == 200:
                            logger.info("Successfully fetched Incapsula script")
                            # Wait a bit for the script to execute
                            time.sleep(5)
                            return True
                    except Exception as e:
                        logger.warning(f"Failed to fetch Incapsula script: {e}")
            
            return False
        return True
    
    def make_request_with_retry(self, url, max_retries=3):
        """
        Make request with retry logic for Incapsula protection
        """
        for attempt in range(max_retries):
            logger.info(f"Attempt {attempt + 1}/{max_retries} for {url}")
            
            try:
                response = self.session.get(url, timeout=30)
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    # Check if we got the actual content or protection page
                    if self.handle_incapsula_protection(response):
                        logger.info("Successfully bypassed protection")
                        return response
                    else:
                        logger.warning(f"Still getting protection page on attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            time.sleep(self.delay * (attempt + 1))  # Increasing delay
                            continue
                else:
                    logger.warning(f"Unexpected status code: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(self.delay)
        
        logger.error("All attempts failed")
        return None
    
    def make_initial_request(self):
        """
        Make the initial request with enhanced protection handling
        """
        try:
            # First, try to access the main court roster page
            logger.info("Accessing main court roster page...")
            main_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
            main_response = self.make_request_with_retry(main_url)
            
            if main_response and main_response.status_code == 200:
                logger.info("Successfully accessed main page")
                time.sleep(self.delay)
                
                # Now try the target page
                logger.info(f"Making request to: {self.target_url}")
                response = self.make_request_with_retry(self.target_url)
                
                if response and response.status_code == 200:
                    logger.info("Successfully retrieved the target page")
                    return response
                else:
                    logger.error("Failed to retrieve target page")
                    return None
            else:
                logger.error("Failed to access main page")
                return None
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def parse_response(self, response):
        """
        Parse the HTML response and extract useful information
        """
        if not response:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract page title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"
        logger.info(f"Page title: {title_text}")
        
        # Check if we're still on protection page
        if 'Incapsula' in response.text or 'SWJIYLWA' in response.text:
            logger.warning("Still on Incapsula protection page")
            return {
                'title': 'Incapsula Protection Page',
                'forms_count': 0,
                'inputs_count': 0,
                'selects_count': 0,
                'links_count': 0,
                'scripts_count': 0,
                'has_viewstate': False,
                'has_event_validation': False,
                'protection_detected': True
            }
        
        # Look for forms (ASP.NET pages often have forms)
        forms = soup.find_all('form')
        logger.info(f"Found {len(forms)} form(s) on the page")
        
        # Look for input fields
        inputs = soup.find_all('input')
        logger.info(f"Found {len(inputs)} input field(s)")
        
        # Look for select dropdowns
        selects = soup.find_all('select')
        logger.info(f"Found {len(selects)} select dropdown(s)")
        
        # Look for links
        links = soup.find_all('a', href=True)
        logger.info(f"Found {len(links)} link(s)")
        
        # Extract any JavaScript that might be relevant
        scripts = soup.find_all('script')
        logger.info(f"Found {len(scripts)} script tag(s)")
        
        # Look for specific ASP.NET elements
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})
        if viewstate:
            logger.info("Found __VIEWSTATE field")
        
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})
        if event_validation:
            logger.info("Found __EVENTVALIDATION field")
        
        return {
            'title': title_text,
            'forms_count': len(forms),
            'inputs_count': len(inputs),
            'selects_count': len(selects),
            'links_count': len(links),
            'scripts_count': len(scripts),
            'has_viewstate': viewstate is not None,
            'has_event_validation': event_validation is not None,
            'protection_detected': False,
            'forms': [{'action': form.get('action'), 'method': form.get('method')} for form in forms],
            'inputs': [{'name': inp.get('name'), 'type': inp.get('type'), 'value': inp.get('value')} for inp in inputs],
            'selects': [{'name': sel.get('name'), 'options': [opt.get('value') for opt in sel.find_all('option')]} for sel in selects]
        }
    
    def save_response(self, response, filename="response_enhanced.html"):
        """
        Save the response content to a file for inspection
        """
        if response:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"Response saved to {filename}")
    
    def run(self):
        """
        Main method to run the enhanced scraper
        """
        logger.info("Starting Enhanced SC Courts scraper...")
        
        # Make the initial request
        response = self.make_initial_request()
        
        if response:
            # Parse the response
            parsed_data = self.parse_response(response)
            
            # Save response for inspection
            self.save_response(response)
            
            # Print summary
            if parsed_data:
                print("\n" + "="*50)
                print("ENHANCED SCRAPING SUMMARY")
                print("="*50)
                print(f"Page Title: {parsed_data['title']}")
                print(f"Forms Found: {parsed_data['forms_count']}")
                print(f"Input Fields: {parsed_data['inputs_count']}")
                print(f"Select Dropdowns: {parsed_data['selects_count']}")
                print(f"Links: {parsed_data['links_count']}")
                print(f"Scripts: {parsed_data['scripts_count']}")
                print(f"Has ViewState: {parsed_data['has_viewstate']}")
                print(f"Has EventValidation: {parsed_data['has_event_validation']}")
                
                if parsed_data.get('protection_detected'):
                    print("\n⚠️ PROTECTION DETECTED:")
                    print("The website is still showing an Incapsula protection page.")
                    print("This is anti-bot protection that's difficult to bypass.")
                    print("\nPossible solutions:")
                    print("1. Try a different US VPN server")
                    print("2. Use a residential proxy service")
                    print("3. Try accessing from a different US location")
                    print("4. Wait and try again later")
                else:
                    print("\n✅ SUCCESS! Real content retrieved!")
                
                if parsed_data.get('forms'):
                    print("\nForms:")
                    for i, form in enumerate(parsed_data['forms']):
                        print(f"  Form {i+1}: Action={form['action']}, Method={form['method']}")
                
                if parsed_data.get('inputs'):
                    print("\nInput Fields:")
                    for inp in parsed_data['inputs'][:10]:  # Show first 10
                        print(f"  Name: {inp['name']}, Type: {inp['type']}, Value: {inp['value']}")
                    if len(parsed_data['inputs']) > 10:
                        print(f"  ... and {len(parsed_data['inputs']) - 10} more")
                
                if parsed_data.get('selects'):
                    print("\nSelect Dropdowns:")
                    for sel in parsed_data['selects']:
                        print(f"  Name: {sel['name']}, Options: {sel['options']}")
            
            return parsed_data
        else:
            logger.error("Failed to retrieve the page")
            return None

def main():
    """
    Main function to run the enhanced scraper
    """
    scraper = SCCourtsScraperEnhanced()
    result = scraper.run()
    
    if result:
        if result.get('protection_detected'):
            print("\n⚠️ Scraping completed but protection detected!")
            print("Check 'response_enhanced.html' for details.")
        else:
            print("\n🎉 Enhanced scraping completed successfully!")
            print("Check 'response_enhanced.html' for the full page content.")
    else:
        print("\n❌ Enhanced scraping failed!")

if __name__ == "__main__":
    main()
