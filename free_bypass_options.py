#!/usr/bin/env python3
"""
Free options to bypass Incapsula protection
"""

import requests
import time
import random
from bs4 import BeautifulSoup
import json

class FreeBypassOptions:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def option_1_different_user_agents(self):
        """
        Option 1: Try different user agents to bypass detection
        """
        print("🔄 Option 1: Trying different user agents...")
        
        user_agents = [
            # Mobile browsers (often less detected)
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            
            # Different desktop browsers
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            
            # Older browsers (sometimes less detected)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
        ]
        
        for i, ua in enumerate(user_agents):
            print(f"  Trying user agent {i+1}/{len(user_agents)}...")
            
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            try:
                response = requests.get(self.target_url, headers=headers, timeout=15)
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS with user agent {i+1}!")
                    return response
                else:
                    print(f"  ❌ Still blocked with user agent {i+1}")
            except Exception as e:
                print(f"  ❌ Error with user agent {i+1}: {e}")
            
            time.sleep(2)  # Be respectful
        
        return None
    
    def option_2_session_simulation(self):
        """
        Option 2: Simulate a real browser session
        """
        print("🔄 Option 2: Simulating real browser session...")
        
        try:
            # First visit the main page like a real user
            print("  Visiting main page first...")
            main_response = self.session.get("https://publicindex.sccourts.org/dorchester/courtrosters/")
            time.sleep(3)  # Wait like a real user
            
            # Then visit the target page
            print("  Now visiting target page...")
            response = self.session.get(self.target_url)
            
            if response.status_code == 200 and 'Incapsula' not in response.text:
                print("  ✅ SUCCESS with session simulation!")
                return response
            else:
                print("  ❌ Still blocked with session simulation")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with session simulation: {e}")
            return None
    
    def option_3_different_headers(self):
        """
        Option 3: Try different header combinations
        """
        print("🔄 Option 3: Trying different header combinations...")
        
        header_combinations = [
            # Minimal headers
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            },
            # Mobile headers
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            # Curl-like headers
            {
                'User-Agent': 'curl/7.68.0',
                'Accept': '*/*'
            }
        ]
        
        for i, headers in enumerate(header_combinations):
            print(f"  Trying header combination {i+1}/{len(header_combinations)}...")
            
            try:
                response = requests.get(self.target_url, headers=headers, timeout=15)
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS with header combination {i+1}!")
                    return response
                else:
                    print(f"  ❌ Still blocked with header combination {i+1}")
            except Exception as e:
                print(f"  ❌ Error with header combination {i+1}: {e}")
            
            time.sleep(2)
        
        return None
    
    def option_4_free_proxy_rotation(self):
        """
        Option 4: Try free proxy rotation
        """
        print("🔄 Option 4: Trying free proxy rotation...")
        
        # Some free proxy sources to try
        free_proxy_sources = [
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=US&format=json"
        ]
        
        proxies = []
        for source in free_proxy_sources:
            try:
                print(f"  Fetching from {source}...")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    if 'json' in source:
                        data = response.json()
                        for proxy_data in data:
                            if isinstance(proxy_data, dict) and 'ip' in proxy_data:
                                proxies.append(f"{proxy_data['ip']}:{proxy_data['port']}")
                    else:
                        for line in response.text.strip().split('\n'):
                            if ':' in line:
                                proxies.append(line.strip())
            except Exception as e:
                print(f"  ❌ Error fetching from {source}: {e}")
        
        if not proxies:
            print("  ❌ No free proxies found")
            return None
        
        print(f"  Found {len(proxies)} free proxies, testing first 5...")
        
        for i, proxy in enumerate(proxies[:5]):
            print(f"  Testing proxy {i+1}: {proxy}")
            
            try:
                proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                response = requests.get(self.target_url, proxies=proxy_dict, timeout=10)
                
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS with proxy {proxy}!")
                    return response
                else:
                    print(f"  ❌ Still blocked with proxy {proxy}")
            except Exception as e:
                print(f"  ❌ Error with proxy {proxy}: {e}")
            
            time.sleep(2)
        
        return None
    
    def option_5_tor_browser_simulation(self):
        """
        Option 5: Simulate Tor browser (often bypasses protection)
        """
        print("🔄 Option 5: Simulating Tor browser...")
        
        tor_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        
        try:
            response = requests.get(self.target_url, headers=tor_headers, timeout=15)
            if response.status_code == 200 and 'Incapsula' not in response.text:
                print("  ✅ SUCCESS with Tor simulation!")
                return response
            else:
                print("  ❌ Still blocked with Tor simulation")
                return None
        except Exception as e:
            print(f"  ❌ Error with Tor simulation: {e}")
            return None
    
    def run_all_options(self):
        """
        Try all free bypass options
        """
        print("🚀 Trying all free bypass options...")
        print("=" * 50)
        
        options = [
            ("Different User Agents", self.option_1_different_user_agents),
            ("Session Simulation", self.option_2_session_simulation),
            ("Different Headers", self.option_3_different_headers),
            ("Free Proxy Rotation", self.option_4_free_proxy_rotation),
            ("Tor Browser Simulation", self.option_5_tor_browser_simulation)
        ]
        
        for name, method in options:
            print(f"\n🔍 {name}")
            print("-" * 30)
            
            try:
                result = method()
                if result:
                    print(f"\n🎉 SUCCESS with {name}!")
                    print("Saving response...")
                    
                    with open(f'success_response_{name.lower().replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                        f.write(result.text)
                    
                    print(f"Response saved to success_response_{name.lower().replace(' ', '_')}.html")
                    return result
                else:
                    print(f"❌ {name} failed")
            except Exception as e:
                print(f"❌ {name} error: {e}")
            
            time.sleep(3)  # Wait between attempts
        
        print("\n❌ All free options failed")
        print("💡 Consider trying a different US VPN server or paid proxy service")
        return None

def main():
    """
    Main function to try all free bypass options
    """
    print("🆓 FREE BYPASS OPTIONS FOR SC COURTS SCRAPER")
    print("=" * 60)
    
    bypass = FreeBypassOptions()
    result = bypass.run_all_options()
    
    if result:
        print("\n🎉 SUCCESS! One of the free options worked!")
        print("You can now use this method for your scraping.")
    else:
        print("\n💡 All free options failed. Consider:")
        print("1. Try a different US VPN server (East Coast)")
        print("2. Use a different VPN provider")
        print("3. Try a residential proxy service")
        print("4. Wait and try again later")

if __name__ == "__main__":
    main()
