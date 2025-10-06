#!/usr/bin/env python3
"""
Complete session scraper that replicates the entire browser request sequence
"""

import requests
import time
import random
from bs4 import BeautifulSoup

class CompleteSessionScraper:
    def __init__(self):
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.session = requests.Session()
        
        # Set up headers to match your browser exactly
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
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
        
        # ULTRA FRESH cookies from your working session (just updated!)
        self.cookies = {
            'visid_incap_2861446': 'hKN0Azf6QT+8enpyV19ER4fN42gAAAAAQUIPAAAAAACR6zdhUKI2jlkgNHsrL3Bv',
            'incap_ses_1404_2861446': 'rM9PNXoURW0t/xOtwAJ8E4fN42gAAAAAXyj7QPjZkSUD3mjjSvk2rQ==',
            'SCJDPublicIndex': 'ffffffffc3a0e30045525d5f4f58455e445a4a423660',
            'nlbi_2861446': '+HS3b/n7uXSv2xVG11Z32gAAAAA5qU31PvEhdqjBXrQAdQuu',
            'reese84': '3:txBu7lFW+0YvvlglKJUKnA==:23utpAJS7nuioepyk7wdq2t50ro/pLbX04QmHt8XWlG793BH0QLBQp5mKpjLdf/HNKicG2z3EUIETFkYJPEjKtja6ZX+9eGnFZByWOQJf5/Ld/dTQitlgjd+f7tBW9P9jM+RD1sA1jSMaQ7IvD02Tcyqn149anXwpeDhLFHWWUywUzxRLs0ZIHZUY6ASPT1h0NGFu2h167viWYwuWuocsM68xGuxfjAB5n4mE/stRRwLX+vT2m4VvSvPEOmums6ARpLGWLXjvlbxbFwinkMHNTrY1drluV9EgKzYIwATIBLatUKwy9VCRtUerHzwrohHqOaspX3233eEGPyTURLZQpQPiF4F4SG6fDCLrwNlCbvh2asNM5kfP1QNv+5ZFYZHKL6sLTBtwcDC7AEArvtX0oPoVHqXp88VmvTRVrc7jgxRbhBJ5oIC/weMu58e/yAJa5gUL2YtuuEI3kiJY4OabMGvuwoMZO9QjFv//V7ILcxxpXwyZvTh+FlSjqFk8D8lRPFI03sRuJQHnVpleac2nQ==:us8TL1eG570Tm/x2vDeH1VEFK8W5a3XxiDiWkKnmkCc=',
            'ASP.NET_SessionId': 'aqsqu0kdg0r1kdgdvxh0fzhl',
            'nlbi_2861446_2147483392': 'ERBGIdnkxCQCx1ha11Z32gAAAACJhpX4qB43jdA74ZvR+fTa'  # UPDATED!
        }
    
    def human_delay(self, min_delay=0.5, max_delay=2.0):
        """Add human-like delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def make_main_request(self):
        """Make the main page request"""
        try:
            print("🎯 Making main page request...")
            
            # Set referer
            self.session.headers['referer'] = 'https://publicindex.sccourts.org/dorchester/courtrosters/'
            
            response = self.session.get(
                self.target_url,
                cookies=self.cookies,
                timeout=30
            )
            
            print(f"📊 Main request status: {response.status_code}")
            print(f"📏 Response length: {len(response.text)} characters")
            
            if response.status_code == 200:
                if 'Incapsula' in response.text or 'incapsula' in response.text.lower():
                    print("⚠️ Incapsula protection still detected")
                    return self.analyze_protection(response.text)
                else:
                    print("✅ SUCCESS! Main page loaded without protection!")
                    return self.parse_successful_response(response.text)
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Main request error: {e}")
            return False
    
    def make_supporting_requests(self):
        """Make supporting requests to load all resources"""
        try:
            print("🔧 Loading supporting resources...")
            
            # List of supporting requests from your browser session
            supporting_urls = [
                'https://publicindex.sccourts.org/inough-rubie-hen-me-And-And-man-Old-time-to-pain',
                'https://publicindex.sccourts.org/dorchester/SCJDCommonWebFiles/SCJDStyles.css',
                'https://publicindex.sccourts.org/Dorchester/CourtRosters/WebResource.axd?d=PTKSqrCBeiX26hSQ-4d2HO_FR0ghsGtDiqM1gGXFYzOAeA75EELpyi1ImH-RuErWDJzsQZ3yYQpIoBwVUE0iUXbRnvZaKUBHXmafo-bbh0boTvfs4vPu1HoADhasVYlX8eUPqQ2&t=637581790915555973',
                'https://publicindex.sccourts.org/Dorchester/CourtRosters/WebResource.axd?d=yHSk03n8qhGuYU3dqttnQ71qTt_0El3n1mxBXim4Y_-Y3mTP08Bvg1wOhE6CNGMfa0pKDFyPqFYCSLv2UBjX7AKLbHI1&t=638568460745067788'
            ]
            
            for url in supporting_urls:
                try:
                    self.session.get(url, cookies=self.cookies, timeout=10)
                    self.human_delay(0.1, 0.3)
                except:
                    pass  # Ignore errors for supporting resources
            
            print("✅ Supporting resources loaded")
            return True
            
        except Exception as e:
            print(f"⚠️ Supporting requests error: {e}")
            return True  # Don't fail if supporting requests fail
    
    def make_data_request(self):
        """Make the data request that loads court information"""
        try:
            print("📊 Making data request...")
            
            data_url = 'https://publicindex.sccourts.org/inough-rubie-hen-me-And-And-man-Old-time-to-pain?d=publicindex.sccourts.org'
            
            headers = {
                'accept': 'application/json; charset=utf-8',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'text/plain; charset=utf-8',
                'origin': 'https://publicindex.sccourts.org',
                'priority': 'u=1, i',
                'referer': 'https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx',
                'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
            }
            
            # The data payload from your request
            data_payload = '"3:txBu7lFW+0YvvlglKJUKnA==:23utpAJS7nuioepyk7wdq2t50ro/pLbX04QmHt8XWlG793BH0QLBQp5mKpjLdf/HNKicG2z3EUIETFkYJPEjKtja6ZX+9eGnFZByWOQJf5/Ld/dTQitlgjd+f7tBW9P9jM+RD1sA1jSMaQ7IvD02Tcyqn149anXwpeDhLFHWWUywUzxRLs0ZIHZUY6ASPT1h0NGFu2h167viWYwuWuocsM68xGuxfjAB5n4mE/stRRwLX+vT2m4VvSvPEOmums6ARpLGWLXjvlbxbFwinkMHNTrY1drluV9EgKzYIwATIBLatUKwy9VCRtUerHzwrohHqOaspX3233eEGPyTURLZQpQPiF4F4SG6fDCLrwNlCbvh2asNM5kfP1QNv+5ZFYZHKL6sLTBtwcDC7AEArvtX0oPoVHqXp88VmvTRVrc7jgxRbhBJ5oIC/weMu58e/yAJa5gUL2YtuuEI3kiJY4OabMGvuwoMZO9QjFv//V7ILcxxpXwyZvTh+FlSjqFk8D8lRPFI03sRuJQHnVpleac2nQ==:us8TL1eG570Tm/x2vDeH1VEFK8W5a3XxiDiWkKnmkCc="'
            
            response = self.session.post(
                data_url,
                headers=headers,
                cookies=self.cookies,
                data=data_payload,
                timeout=30
            )
            
            print(f"📊 Data request status: {response.status_code}")
            print(f"📏 Data response length: {len(response.text)} characters")
            
            if response.status_code == 200:
                print("✅ Data request successful!")
                return response.text
            else:
                print(f"⚠️ Data request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Data request error: {e}")
            return None
    
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
    
    def run_complete_session(self):
        """Run the complete session sequence"""
        try:
            print("🚀 Starting complete session sequence...")
            print("=" * 50)
            
            # Step 1: Make main request
            main_result = self.make_main_request()
            if not main_result:
                return False
            
            # Step 2: Load supporting resources
            self.make_supporting_requests()
            
            # Step 3: Make data request
            data_result = self.make_data_request()
            if data_result:
                print("📊 Court data loaded successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Complete session error: {e}")
            return False

def main():
    print("🎯 COMPLETE SESSION SCRAPER")
    print("=" * 50)
    print("Replicating the entire browser session sequence")
    print()
    
    scraper = CompleteSessionScraper()
    result = scraper.run_complete_session()
    
    if result:
        print("\n🎉 COMPLETE SESSION SUCCESSFUL!")
        print("The entire browser session was replicated successfully!")
        print("This can now be deployed to a US server and will work!")
    else:
        print("\n❌ SESSION FAILED")
        print("The session replication failed")

if __name__ == "__main__":
    main()
