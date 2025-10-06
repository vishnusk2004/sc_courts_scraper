#!/usr/bin/env python3
"""
Human-like scraper to bypass Incapsula robot detection
"""

import requests
import time
import random
from bs4 import BeautifulSoup

class HumanLikeScraper:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.session = requests.Session()
        
        # Human-like headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
    
    def human_delay(self, min_delay=1, max_delay=3):
        """Add human-like delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def simulate_human_browsing(self):
        """Simulate human browsing patterns"""
        try:
            # Step 1: Visit main SC Courts page first
            print("🌐 Step 1: Visiting main SC Courts page...")
            main_url = "https://publicindex.sccourts.org/"
            response = self.session.get(main_url, timeout=30)
            print(f"   Status: {response.status_code}")
            self.human_delay(2, 4)
            
            # Step 2: Visit Dorchester county page
            print("🌐 Step 2: Visiting Dorchester county page...")
            county_url = "https://publicindex.sccourts.org/dorchester/"
            response = self.session.get(county_url, timeout=30)
            print(f"   Status: {response.status_code}")
            self.human_delay(2, 4)
            
            # Step 3: Visit court rosters page
            print("🌐 Step 3: Visiting court rosters page...")
            rosters_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
            response = self.session.get(rosters_url, timeout=30)
            print(f"   Status: {response.status_code}")
            self.human_delay(3, 5)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in human browsing simulation: {e}")
            return False
    
    def scrape_with_human_behavior(self):
        """Scrape with human-like behavior"""
        try:
            print("🤖 Starting human-like scraping...")
            
            # Simulate human browsing first
            if not self.simulate_human_browsing():
                print("⚠️ Human browsing simulation failed, proceeding anyway")
            
            # Add random mouse movement simulation
            print("🖱️ Simulating mouse movements...")
            self.human_delay(1, 2)
            
            # Make the actual request with human-like timing
            print("🎯 Making target request...")
            self.human_delay(2, 4)
            
            response = self.session.get(self.target_url, timeout=30)
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                if 'Incapsula' in response.text:
                    print("⚠️ Still getting Incapsula protection")
                    return self.analyze_protection(response.text)
                else:
                    print("✅ SUCCESS! No protection detected!")
                    return self.parse_successful_response(response.text)
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Scraping error: {e}")
            return False
    
    def analyze_protection(self, html_content):
        """Analyze the protection page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("\n🔍 PROTECTION ANALYSIS:")
        print("=" * 40)
        
        # Check for specific protection indicators
        if 'Incapsula' in html_content:
            print("🛡️ Incapsula protection detected")
        
        if 'incident_id' in html_content:
            print("🆔 Incident ID found in response")
        
        if 'iframe' in html_content:
            print("🖼️ Iframe-based protection detected")
        
        # Extract page title
        title = soup.title.get_text(strip=True) if soup.title else 'No title'
        print(f"📄 Page title: {title}")
        
        # Check for specific text
        page_text = soup.get_text()
        if 'Request unsuccessful' in page_text:
            print("❌ 'Request unsuccessful' message detected")
        
        if 'incident ID' in page_text:
            print("🆔 Incident ID message detected")
        
        return False
    
    def parse_successful_response(self, html_content):
        """Parse successful response"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("\n✅ SUCCESSFUL RESPONSE ANALYSIS:")
        print("=" * 40)
        
        # Count elements
        forms = soup.find_all('form')
        inputs = soup.find_all('input')
        links = soup.find_all('a')
        scripts = soup.find_all('script')
        
        print(f"📝 Forms found: {len(forms)}")
        print(f"🔍 Inputs found: {len(inputs)}")
        print(f"🔗 Links found: {len(links)}")
        print(f"📜 Scripts found: {len(scripts)}")
        
        # Show page title
        title = soup.title.get_text(strip=True) if soup.title else 'No title'
        print(f"📄 Page title: {title}")
        
        return True

def main():
    print("🤖 HUMAN-LIKE SCRAPER FOR SC COURTS")
    print("=" * 50)
    
    scraper = HumanLikeScraper()
    result = scraper.scrape_with_human_behavior()
    
    if result:
        print("\n🎉 SCRAPING SUCCESSFUL!")
    else:
        print("\n❌ SCRAPING FAILED - Protection still active")

if __name__ == "__main__":
    main()
