#!/usr/bin/env python3
"""
South Carolina Courts Scraper
Scrapes court roster information from publicindex.sccourts.org
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

class SCCourtsScraper:
    def __init__(self, use_proxy=False, proxy_list=None):
        self.session = requests.Session()
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        
        # Set up headers based on the request details provided
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
        
        # Add some delay to be more respectful
        self.delay = 2
        
        # US-based proxy list (free proxies - may not always work)
        if not self.proxy_list:
            # Try to load from file first
            try:
                with open('us_proxies.txt', 'r') as f:
                    proxy_strings = [line.strip() for line in f if line.strip()]
                    self.proxy_list = [
                        {'http': f'http://{proxy}', 'https': f'http://{proxy}'} 
                        for proxy in proxy_strings
                    ]
                logger.info(f"Loaded {len(self.proxy_list)} proxies from us_proxies.txt")
            except FileNotFoundError:
                logger.info("No us_proxies.txt found, will try without proxies")
                self.proxy_list = []
    
    def get_random_proxy(self):
        """
        Get a random proxy from the list
        """
        if self.proxy_list:
            return random.choice(self.proxy_list)
        return None
    
    def test_proxy(self, proxy):
        """
        Test if a proxy is working
        """
        try:
            test_url = "http://httpbin.org/ip"
            response = requests.get(test_url, proxies=proxy, timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                logger.info(f"Proxy working, IP: {ip_info.get('origin', 'Unknown')}")
                return True
        except Exception as e:
            logger.warning(f"Proxy test failed: {e}")
        return False
    
    def make_request_with_proxy(self, url, proxy=None):
        """
        Make a request with optional proxy
        """
        try:
            if proxy:
                logger.info(f"Using proxy: {proxy}")
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
        Make the initial request to RosterSelection.aspx
        """
        try:
            # Try different approaches
            approaches = [
                ("Direct request", None),
                ("With random proxy", self.get_random_proxy() if self.use_proxy else None)
            ]
            
            for approach_name, proxy in approaches:
                logger.info(f"Trying approach: {approach_name}")
                
                # First, try to access the main court roster page to establish session
                logger.info("First, accessing the main court roster page...")
                main_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
                main_response = self.make_request_with_proxy(main_url, proxy)
                
                if main_response:
                    logger.info(f"Main page response status: {main_response.status_code}")
                    
                    if main_response.status_code == 200:
                        logger.info("Successfully accessed main page, now trying target page...")
                        time.sleep(self.delay)  # Add delay between requests
                    else:
                        logger.warning(f"Main page returned status {main_response.status_code}, proceeding anyway...")
                    
                    # Now try the target page
                    logger.info(f"Making request to: {self.target_url}")
                    response = self.make_request_with_proxy(self.target_url, proxy)
                    
                    if response:
                        logger.info(f"Response status: {response.status_code}")
                        logger.info(f"Response headers: {dict(response.headers)}")
                        
                        if response.status_code == 200:
                            logger.info("Successfully retrieved the page")
                            return response
                        elif response.status_code == 403:
                            logger.warning("Received 403 Forbidden - the site may have anti-bot protection")
                            # Try to save the response anyway to see what we get
                            self.save_response(response, f"403_response_{approach_name.replace(' ', '_')}.html")
                            # Continue to next approach
                            continue
                        else:
                            logger.error(f"Failed to retrieve page. Status code: {response.status_code}")
                            continue
                
                # If we get here, this approach failed, try next one
                logger.info(f"Approach '{approach_name}' failed, trying next...")
                time.sleep(1)
            
            # If all approaches failed
            logger.error("All approaches failed")
            return None
                
        except requests.exceptions.RequestException as e:
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
    
    def try_alternative_approach(self):
        """
        Try alternative approaches if the main method fails
        """
        logger.info("Trying alternative approach...")
        
        # Try different user agents that might be more US-focused
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        ]
        
        for i, ua in enumerate(user_agents):
            logger.info(f"Trying user agent {i+1}: {ua[:50]}...")
            self.session.headers.update({'User-Agent': ua})
            
            # Try accessing the base URL first
            try:
                base_response = self.session.get(self.base_url)
                logger.info(f"Base URL response: {base_response.status_code}")
                time.sleep(2)
                
                # Now try the target
                response = self.session.get(self.target_url)
                logger.info(f"Alternative approach response: {response.status_code}")
                
                if response.status_code == 200:
                    return response
                else:
                    self.save_response(response, f"alternative_response_ua{i+1}.html")
                    if response.status_code != 403:  # If it's not 403, this might be progress
                        return response
                    
            except Exception as e:
                logger.error(f"Alternative approach {i+1} failed: {e}")
                continue
        
        return None

    def run(self):
        """
        Main method to run the scraper
        """
        logger.info("Starting SC Courts scraper...")
        
        # Make the initial request
        response = self.make_initial_request()
        
        # If we got a 403 or other error, try alternative approach
        if not response or response.status_code != 200:
            logger.info("Initial request failed, trying alternative approach...")
            response = self.try_alternative_approach()
        
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
            logger.error("Failed to retrieve the page")
            return None

def main():
    """
    Main function to run the scraper
    """
    import sys
    
    # Check if user wants to use proxies
    use_proxy = '--proxy' in sys.argv or '--use-proxy' in sys.argv
    
    if use_proxy:
        print("Attempting to find US proxies first...")
        try:
            from proxy_finder import USProxyFinder
            finder = USProxyFinder()
            proxies = finder.find_working_proxies(max_proxies=3)
            if proxies:
                print(f"Found {len(proxies)} working US proxies")
            else:
                print("No working US proxies found, proceeding without proxies")
        except Exception as e:
            print(f"Error finding proxies: {e}")
            print("Proceeding without proxies")
    
    scraper = SCCourtsScraper(use_proxy=use_proxy)
    result = scraper.run()
    
    if result:
        print("\nScraping completed successfully!")
        print("Check 'response.html' for the full page content.")
    else:
        print("Scraping failed!")
        print("\nTroubleshooting tips:")
        print("1. Try running with --proxy flag: python sc_courts_scraper.py --proxy")
        print("2. The site may be blocking non-US IP addresses")
        print("3. Consider using a VPN with US location")
        print("4. Check the saved response files for more details")

if __name__ == "__main__":
    main()
