#!/usr/bin/env python3
"""
Advanced techniques to bypass Incapsula protection
"""

import requests
import time
import random
from bs4 import BeautifulSoup
import re

class IncapsulaBypass:
    def __init__(self):
        self.session = requests.Session()
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def method_1_incapsula_script_bypass(self):
        """
        Method 1: Try to execute the Incapsula script
        """
        print("🔧 Method 1: Incapsula script bypass...")
        
        try:
            # First get the protection page
            response = self.session.get(self.target_url, timeout=30)
            if response.status_code == 200 and 'Incapsula' in response.text:
                print("  Found Incapsula protection page")
                
                # Extract the script URL
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', src=re.compile(r'_Incapsula_Resource'))
                
                if script_tag:
                    script_url = script_tag.get('src')
                    if script_url:
                        full_script_url = f"https://publicindex.sccourts.org{script_url}"
                        print(f"  Found script URL: {full_script_url}")
                        
                        # Try to fetch the script
                        script_response = self.session.get(full_script_url, timeout=30)
                        if script_response.status_code == 200:
                            print("  Successfully fetched Incapsula script")
                            
                            # Wait for script to execute
                            time.sleep(5)
                            
                            # Try the target page again
                            retry_response = self.session.get(self.target_url, timeout=30)
                            if retry_response.status_code == 200 and 'Incapsula' not in retry_response.text:
                                print("  ✅ SUCCESS! Incapsula script bypass worked!")
                                return retry_response
                            else:
                                print("  ❌ Still blocked after script execution")
                        else:
                            print("  ❌ Could not fetch Incapsula script")
                    else:
                        print("  ❌ No script URL found")
                else:
                    print("  ❌ No Incapsula script found")
            else:
                print("  ❌ Not getting Incapsula protection page")
                
        except Exception as e:
            print(f"  ❌ Error with script bypass: {e}")
        
        return None
    
    def method_2_session_persistence(self):
        """
        Method 2: Build session persistence
        """
        print("🔗 Method 2: Session persistence...")
        
        try:
            # Step 1: Visit main page
            print("  Step 1: Visiting main page...")
            main_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
            main_response = self.session.get(main_url, timeout=30)
            print(f"  Main page status: {main_response.status_code}")
            
            # Wait like a human
            time.sleep(random.uniform(3, 7))
            
            # Step 2: Visit intermediate page
            print("  Step 2: Visiting intermediate page...")
            intermediate_url = "https://publicindex.sccourts.org/dorchester/"
            intermediate_response = self.session.get(intermediate_url, timeout=30)
            print(f"  Intermediate status: {intermediate_response.status_code}")
            
            # Wait again
            time.sleep(random.uniform(2, 5))
            
            # Step 3: Visit target page
            print("  Step 3: Visiting target page...")
            target_response = self.session.get(self.target_url, timeout=30)
            print(f"  Target status: {target_response.status_code}")
            
            if target_response.status_code == 200 and 'Incapsula' not in target_response.text:
                print("  ✅ SUCCESS! Session persistence worked!")
                return target_response
            else:
                print("  ❌ Still blocked with session persistence")
                
        except Exception as e:
            print(f"  ❌ Error with session persistence: {e}")
        
        return None
    
    def method_3_different_headers(self):
        """
        Method 3: Try different header combinations
        """
        print("📋 Method 3: Different headers...")
        
        header_combinations = [
            # Minimal headers
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            },
            # Mobile headers
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            # Curl-like headers
            {
                'User-Agent': 'curl/7.68.0',
                'Accept': '*/*'
            },
            # Old browser headers
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        ]
        
        for i, headers in enumerate(header_combinations):
            print(f"  Trying header combination {i+1}/{len(header_combinations)}...")
            
            try:
                response = self.session.get(self.target_url, headers=headers, timeout=30)
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS with header combination {i+1}!")
                    return response
                else:
                    print(f"  ❌ Still blocked with header combination {i+1}")
            except Exception as e:
                print(f"  ❌ Error with header combination {i+1}: {e}")
            
            time.sleep(2)
        
        return None
    
    def method_4_wait_and_retry(self):
        """
        Method 4: Wait and retry (time-based bypass)
        """
        print("⏰ Method 4: Wait and retry...")
        
        wait_times = [30, 60, 120]  # 30 seconds to 2 minutes
        
        for wait_time in wait_times:
            print(f"  Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
            try:
                response = self.session.get(self.target_url, timeout=30)
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS after {wait_time}s wait!")
                    return response
                else:
                    print(f"  ❌ Still blocked after {wait_time}s wait")
            except Exception as e:
                print(f"  ❌ Error after {wait_time}s wait: {e}")
        
        return None
    
    def method_5_stealth_mode(self):
        """
        Method 5: Stealth mode simulation
        """
        print("🥷 Method 5: Stealth mode simulation...")
        
        # Headers that simulate stealth mode
        stealth_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1'
        }
        
        try:
            # Try stealth approach
            print("  Trying stealth approach...")
            response = self.session.get(self.target_url, headers=stealth_headers, timeout=30)
            
            if response.status_code == 200 and 'Incapsula' not in response.text:
                print("  ✅ SUCCESS with stealth mode!")
                return response
            else:
                print("  ❌ Still blocked with stealth mode")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with stealth mode: {e}")
            return None
    
    def run_all_methods(self):
        """
        Try all bypass methods
        """
        print("🚀 INCAPSULA BYPASS METHODS")
        print("=" * 50)
        
        methods = [
            ("Incapsula Script Bypass", self.method_1_incapsula_script_bypass),
            ("Session Persistence", self.method_2_session_persistence),
            ("Different Headers", self.method_3_different_headers),
            ("Wait and Retry", self.method_4_wait_and_retry),
            ("Stealth Mode", self.method_5_stealth_mode)
        ]
        
        for name, method in methods:
            print(f"\n🔍 {name}")
            print("-" * 40)
            
            try:
                result = method()
                if result:
                    print(f"\n🎉 SUCCESS with {name}!")
                    print("Saving response...")
                    
                    with open(f'success_{name.lower().replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                        f.write(result.text)
                    
                    print(f"Response saved to success_{name.lower().replace(' ', '_')}.html")
                    return result
                else:
                    print(f"❌ {name} failed")
            except Exception as e:
                print(f"❌ {name} error: {e}")
            
            time.sleep(2)  # Wait between methods
        
        print("\n❌ All bypass methods failed")
        print("💡 The Incapsula protection is very strong.")
        print("Consider trying:")
        print("1. Different US VPN server")
        print("2. Different time of day")
        print("3. Residential proxy service")
        return None

def main():
    """
    Main function to try all bypass methods
    """
    print("🔬 INCAPSULA BYPASS TECHNIQUES")
    print("=" * 60)
    
    bypass = IncapsulaBypass()
    result = bypass.run_all_methods()
    
    if result:
        print("\n🎉 SUCCESS! One of the bypass methods worked!")
        print("You can now use this method for your scraping.")
    else:
        print("\n💡 All bypass methods failed.")
        print("The Incapsula protection is very sophisticated.")
        print("Consider trying a different approach or time.")

if __name__ == "__main__":
    main()
