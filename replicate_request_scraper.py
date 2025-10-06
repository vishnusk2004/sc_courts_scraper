#!/usr/bin/env python3
"""
Replicate the exact working request from browser
"""

import requests
import time
from bs4 import BeautifulSoup

class ReplicateRequestScraper:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.session = requests.Session()
        
        # Set up the exact headers from your working request
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://publicindex.sccourts.org/dorchester/courtrosters/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        })
        
        # Set the exact cookies from your working request (FRESH COOKIES!)
        self.cookies = {
            'visid_incap_2861446': 'hKN0Azf6QT+8enpyV19ER4fN42gAAAAAQUIPAAAAAACR6zdhUKI2jlkgNHsrL3Bv',
            'incap_ses_1404_2861446': 'rM9PNXoURW0t/xOtwAJ8E4fN42gAAAAAXyj7QPjZkSUD3mjjSvk2rQ==',
            'SCJDPublicIndex': 'ffffffffc3a0e30045525d5f4f58455e445a4a423660',
            'nlbi_2861446': '+HS3b/n7uXSv2xVG11Z32gAAAAA5qU31PvEhdqjBXrQAdQuu',
            'reese84': '3:txBu7lFW+0YvvlglKJUKnA==:23utpAJS7nuioepyk7wdq2t50ro/pLbX04QmHt8XWlG793BH0QLBQp5mKpjLdf/HNKicG2z3EUIETFkYJPEjKtja6ZX+9eGnFZByWOQJf5/Ld/dTQitlgjd+f7tBW9P9jM+RD1sA1jSMaQ7IvD02Tcyqn149anXwpeDhLFHWWUywUzxRLs0ZIHZUY6ASPT1h0NGFu2h167viWYwuWuocsM68xGuxfjAB5n4mE/stRRwLX+vT2m4VvSvPEOmums6ARpLGWLXjvlbxbFwinkMHNTrY1drluV9EgKzYIwATIBLatUKwy9VCRtUerHzwrohHqOaspX3233eEGPyTURLZQpQPiF4F4SG6fDCLrwNlCbvh2asNM5kfP1QNv+5ZFYZHKL6sLTBtwcDC7AEArvtX0oPoVHqXp88VmvTRVrc7jgxRbhBJ5oIC/weMu58e/yAJa5gUL2YtuuEI3kiJY4OabMGvuwoMZO9QjFv//V7ILcxxpXwyZvTh+FlSjqFk8D8lRPFI03sRuJQHnVpleac2nQ==:us8TL1eG570Tm/x2vDeH1VEFK8W5a3XxiDiWkKnmkCc=',
            'ASP.NET_SessionId': 'aqsqu0kdg0r1kdgdvxh0fzhl',  # FRESH SESSION COOKIE!
            'nlbi_2861446_2147483392': 'zwn1aWMv2BkSFiBI11Z32gAAAAA6siGRdo/hJELFJov/qqoZ'
        }
    
    def make_request(self):
        """Make the exact request that works in your browser"""
        try:
            print("🚀 Making request with exact browser headers and cookies...")
            print(f"🎯 Target URL: {self.target_url}")
            
            # Make the request with exact cookies and headers
            response = self.session.get(
                self.target_url, 
                cookies=self.cookies,
                timeout=30
            )
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📏 Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                # Check for Incapsula protection
                if 'Incapsula' in response.text or 'incapsula' in response.text.lower():
                    print("⚠️ Incapsula protection still detected")
                    return self.analyze_protection(response.text)
                else:
                    print("✅ SUCCESS! No protection detected!")
                    return self.parse_successful_response(response.text)
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            return False
    
    def analyze_protection(self, html_content):
        """Analyze protection page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("\n🔍 PROTECTION ANALYSIS:")
        print("=" * 40)
        
        title = soup.title.get_text(strip=True) if soup.title else 'No title'
        print(f"📄 Page title: {title}")
        
        if 'Request unsuccessful' in html_content:
            print("❌ 'Request unsuccessful' message detected")
        
        if 'incident_id' in html_content:
            print("🆔 Incident ID found in response")
        
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
        tables = soup.find_all('table')
        
        print(f"📝 Forms found: {len(forms)}")
        print(f"🔍 Inputs found: {len(inputs)}")
        print(f"🔗 Links found: {len(links)}")
        print(f"📜 Scripts found: {len(scripts)}")
        print(f"📊 Tables found: {len(tables)}")
        
        # Show page title
        title = soup.title.get_text(strip=True) if soup.title else 'No title'
        print(f"📄 Page title: {title}")
        
        # Look for court data
        if tables:
            print(f"\n🏛️ COURT DATA FOUND:")
            for i, table in enumerate(tables[:3]):  # Show first 3 tables
                rows = table.find_all('tr')
                print(f"   Table {i+1}: {len(rows)} rows")
                if rows:
                    # Show first row as example
                    first_row = rows[0].get_text(strip=True)
                    print(f"   First row: {first_row[:100]}...")
        
        # Look for specific court-related content
        page_text = soup.get_text()
        if 'court' in page_text.lower() or 'roster' in page_text.lower():
            print("🏛️ Court-related content detected!")
        
        return True

def main():
    print("🎯 REPLICATE REQUEST SCRAPER")
    print("=" * 50)
    print("Using exact headers and cookies from your working browser session")
    print()
    
    scraper = ReplicateRequestScraper()
    result = scraper.make_request()
    
    if result:
        print("\n🎉 SCRAPING SUCCESSFUL!")
        print("The request worked - we can now replicate this from any server!")
    else:
        print("\n❌ SCRAPING FAILED - Protection still active")
        print("The cookies might have expired or the session is invalid")

if __name__ == "__main__":
    main()
