#!/usr/bin/env python3
"""
South Carolina Courts Scraper with Authenticated Proxy Support
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SCCourtsScraperAuthenticated:
    def __init__(self, proxy_list=None):
        self.session = requests.Session()
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.proxy_list = proxy_list or []
        
        # Set up headers
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
        self.delay = 2
    
    def load_authenticated_proxies(self):
        """
        Load authenticated proxies from the list you provided
        """
        # Your authenticated proxy list
        proxy_data = [
            "45.43.190.72:6590:nxhkryfv:fre3i4dn5dvq",
            "64.137.49.92:6633:nxhkryfv:fre3i4dn5dvq",
            "104.238.9.181:6634:nxhkryfv:fre3i4dn5dvq",
            "154.92.116.177:6489:nxhkryfv:fre3i4dn5dvq",
            "185.213.242.108:8572:nxhkryfv:fre3i4dn5dvq",
            "91.212.100.78:6654:nxhkryfv:fre3i4dn5dvq",
            "104.239.41.106:6461:nxhkryfv:fre3i4dn5dvq",
            "45.43.185.178:6184:nxhkryfv:fre3i4dn5dvq",
            "107.152.214.117:8694:nxhkryfv:fre3i4dn5dvq",
            "198.20.191.145:7201:nxhkryfv:fre3i4dn5dvq"
        ]
        
        authenticated_proxies = []
        for proxy_line in proxy_data:
            parts = proxy_line.strip().split(':')
            if len(parts) == 4:
                ip, port, username, password = parts
                proxy_url = f"http://{username}:{password}@{ip}:{port}"
                authenticated_proxies.append({
                    'http': proxy_url,
                    'https': proxy_url
                })
        
        logger.info(f"Loaded {len(authenticated_proxies)} authenticated proxies")
        return authenticated_proxies
    
    def test_proxy(self, proxy):
        """
        Test if a proxy is working
        """
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                origin_ip = ip_info.get('origin', '')
                logger.info(f"Proxy working, IP: {origin_ip}")
                return True
        except Exception as e:
            logger.warning(f"Proxy test failed: {e}")
        return False
    
    def make_request_with_proxy(self, url, proxy=None):
        """
        Make a request with optional authenticated proxy
        """
        try:
            if proxy:
                logger.info(f"Using authenticated proxy: {proxy['http'][:50]}...")
                response = self.session.get(url, proxies=proxy, timeout=30)
            else:
                response = self.session.get(url, timeout=30)
            
            logger.info(f"Response status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def make_initial_request(self):
        """
        Make the initial request to RosterSelection.aspx with proxy rotation
        """
        # Load authenticated proxies
        authenticated_proxies = self.load_authenticated_proxies()
        
        if not authenticated_proxies:
            logger.error("No authenticated proxies available")
            return None
        
        # Try each proxy
        for i, proxy in enumerate(authenticated_proxies):
            logger.info(f"Trying proxy {i+1}/{len(authenticated_proxies)}")
            
            # Test proxy first
            if not self.test_proxy(proxy):
                logger.warning(f"Proxy {i+1} failed connectivity test, skipping")
                continue
            
            # First, try to access the main court roster page
            logger.info("Accessing main court roster page...")
            main_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
            main_response = self.make_request_with_proxy(main_url, proxy)
            
            if main_response and main_response.status_code == 200:
                logger.info("Successfully accessed main page with proxy")
                time.sleep(self.delay)
                
                # Now try the target page
                logger.info(f"Making request to: {self.target_url}")
                response = self.make_request_with_proxy(self.target_url, proxy)
                
                if response:
                    logger.info(f"Response status: {response.status_code}")
                    logger.info(f"Response headers: {dict(response.headers)}")
                    
                    if response.status_code == 200:
                        logger.info("Successfully retrieved the page with authenticated proxy!")
                        return response
                    elif response.status_code == 403:
                        logger.warning("Still getting 403 - this proxy might not be US-based")
                        continue
                    else:
                        logger.error(f"Unexpected status code: {response.status_code}")
                        continue
            else:
                logger.warning(f"Main page failed with proxy {i+1}, trying next...")
                continue
        
        logger.error("All authenticated proxies failed")
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
            'forms': [{'action': form.get('action'), 'method': form.get('method')} for form in forms],
            'inputs': [{'name': inp.get('name'), 'type': inp.get('type'), 'value': inp.get('value')} for inp in inputs],
            'selects': [{'name': sel.get('name'), 'options': [opt.get('value') for opt in sel.find_all('option')]} for sel in selects]
        }
    
    def save_response(self, response, filename="response.html"):
        """
        Save the response content to a file for inspection
        """
        if response:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"Response saved to {filename}")
    
    def run(self):
        """
        Main method to run the scraper with authenticated proxies
        """
        logger.info("Starting SC Courts scraper with authenticated proxies...")
        
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
                print("SCRAPING SUMMARY")
                print("="*50)
                print(f"Page Title: {parsed_data['title']}")
                print(f"Forms Found: {parsed_data['forms_count']}")
                print(f"Input Fields: {parsed_data['inputs_count']}")
                print(f"Select Dropdowns: {parsed_data['selects_count']}")
                print(f"Links: {parsed_data['links_count']}")
                print(f"Scripts: {parsed_data['scripts_count']}")
                print(f"Has ViewState: {parsed_data['has_viewstate']}")
                print(f"Has EventValidation: {parsed_data['has_event_validation']}")
                
                if parsed_data['forms']:
                    print("\nForms:")
                    for i, form in enumerate(parsed_data['forms']):
                        print(f"  Form {i+1}: Action={form['action']}, Method={form['method']}")
                
                if parsed_data['inputs']:
                    print("\nInput Fields:")
                    for inp in parsed_data['inputs'][:10]:  # Show first 10
                        print(f"  Name: {inp['name']}, Type: {inp['type']}, Value: {inp['value']}")
                    if len(parsed_data['inputs']) > 10:
                        print(f"  ... and {len(parsed_data['inputs']) - 10} more")
                
                if parsed_data['selects']:
                    print("\nSelect Dropdowns:")
                    for sel in parsed_data['selects']:
                        print(f"  Name: {sel['name']}, Options: {sel['options']}")
            
            return parsed_data
        else:
            logger.error("Failed to retrieve the page with any proxy")
            return None

def main():
    """
    Main function to run the scraper with authenticated proxies
    """
    print("SC Courts Scraper with Authenticated Proxies")
    print("=" * 50)
    
    scraper = SCCourtsScraperAuthenticated()
    result = scraper.run()
    
    if result:
        print("\n🎉 Scraping completed successfully!")
        print("Check 'response.html' for the full page content.")
    else:
        print("\n❌ Scraping failed!")
        print("The authenticated proxies might be:")
        print("- Expired or inactive")
        print("- Not US-based")
        print("- Blocked by the target website")
        print("- Require different authentication")

if __name__ == "__main__":
    main()
