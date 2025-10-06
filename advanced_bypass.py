#!/usr/bin/env python3
"""
Advanced bypass techniques for Incapsula protection
"""

import requests
import time
import random
from bs4 import BeautifulSoup
import json
import re

class AdvancedBypass:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def method_1_slow_requests(self):
        """
        Method 1: Very slow, human-like requests
        """
        print("🐌 Method 1: Slow human-like requests...")
        
        # Very slow headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        try:
            # Step 1: Visit main page very slowly
            print("  Step 1: Visiting main page...")
            main_url = "https://publicindex.sccourts.org/dorchester/courtrosters/"
            response1 = self.session.get(main_url, headers=headers, timeout=30)
            print(f"  Main page status: {response1.status_code}")
            
            # Wait like a human
            time.sleep(random.uniform(3, 7))
            
            # Step 2: Visit target page very slowly
            print("  Step 2: Visiting target page...")
            response2 = self.session.get(self.target_url, headers=headers, timeout=30)
            print(f"  Target page status: {response2.status_code}")
            
            if response2.status_code == 200 and 'Incapsula' not in response2.text:
                print("  ✅ SUCCESS with slow requests!")
                return response2
            else:
                print("  ❌ Still blocked with slow requests")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with slow requests: {e}")
            return None
    
    def method_2_mobile_simulation(self):
        """
        Method 2: Simulate mobile device
        """
        print("📱 Method 2: Mobile device simulation...")
        
        mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        
        try:
            response = self.session.get(self.target_url, headers=mobile_headers, timeout=30)
            print(f"  Mobile response status: {response.status_code}")
            
            if response.status_code == 200 and 'Incapsula' not in response.text:
                print("  ✅ SUCCESS with mobile simulation!")
                return response
            else:
                print("  ❌ Still blocked with mobile simulation")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with mobile simulation: {e}")
            return None
    
    def method_3_curl_simulation(self):
        """
        Method 3: Simulate curl requests
        """
        print("🔧 Method 3: Curl simulation...")
        
        curl_headers = {
            'User-Agent': 'curl/7.68.0',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        try:
            response = self.session.get(self.target_url, headers=curl_headers, timeout=30)
            print(f"  Curl response status: {response.status_code}")
            
            if response.status_code == 200 and 'Incapsula' not in response.text:
                print("  ✅ SUCCESS with curl simulation!")
                return response
            else:
                print("  ❌ Still blocked with curl simulation")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with curl simulation: {e}")
            return None
    
    def method_4_different_ports(self):
        """
        Method 4: Try different ports (if any)
        """
        print("🔌 Method 4: Different ports...")
        
        # Try different ports if they exist
        ports_to_try = [80, 443, 8080, 8443]
        
        for port in ports_to_try:
            try:
                if port == 443:
                    url = f"https://publicindex.sccourts.org:{port}/dorchester/courtrosters/RosterSelection.aspx"
                else:
                    url = f"http://publicindex.sccourts.org:{port}/dorchester/courtrosters/RosterSelection.aspx"
                
                print(f"  Trying port {port}...")
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS with port {port}!")
                    return response
                else:
                    print(f"  ❌ Port {port} blocked")
                    
            except Exception as e:
                print(f"  ❌ Port {port} error: {e}")
        
        return None
    
    def method_5_wait_and_retry(self):
        """
        Method 5: Wait and retry (time-based bypass)
        """
        print("⏰ Method 5: Wait and retry...")
        
        # Wait different amounts of time
        wait_times = [30, 60, 120, 300]  # 30 seconds to 5 minutes
        
        for wait_time in wait_times:
            print(f"  Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
            try:
                response = self.session.get(self.target_url, timeout=30)
                print(f"  Response status after {wait_time}s wait: {response.status_code}")
                
                if response.status_code == 200 and 'Incapsula' not in response.text:
                    print(f"  ✅ SUCCESS after {wait_time}s wait!")
                    return response
                else:
                    print(f"  ❌ Still blocked after {wait_time}s wait")
                    
            except Exception as e:
                print(f"  ❌ Error after {wait_time}s wait: {e}")
        
        return None
    
    def method_6_browser_automation_simulation(self):
        """
        Method 6: Simulate browser automation
        """
        print("🤖 Method 6: Browser automation simulation...")
        
        # Headers that mimic browser automation tools
        automation_headers = {
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
            'Pragma': 'no-cache'
        }
        
        try:
            # Simulate browser automation behavior
            print("  Simulating browser automation...")
            
            # First request
            response1 = self.session.get(self.base_url, headers=automation_headers, timeout=30)
            time.sleep(2)
            
            # Second request
            response2 = self.session.get(f"{self.base_url}/dorchester/", headers=automation_headers, timeout=30)
            time.sleep(2)
            
            # Third request (target)
            response3 = self.session.get(self.target_url, headers=automation_headers, timeout=30)
            
            if response3.status_code == 200 and 'Incapsula' not in response3.text:
                print("  ✅ SUCCESS with browser automation simulation!")
                return response3
            else:
                print("  ❌ Still blocked with browser automation simulation")
                return None
                
        except Exception as e:
            print(f"  ❌ Error with browser automation simulation: {e}")
            return None
    
    def run_all_methods(self):
        """
        Try all advanced bypass methods
        """
        print("🚀 ADVANCED BYPASS METHODS")
        print("=" * 50)
        
        methods = [
            ("Slow Human-like Requests", self.method_1_slow_requests),
            ("Mobile Device Simulation", self.method_2_mobile_simulation),
            ("Curl Simulation", self.method_3_curl_simulation),
            ("Different Ports", self.method_4_different_ports),
            ("Wait and Retry", self.method_5_wait_and_retry),
            ("Browser Automation Simulation", self.method_6_browser_automation_simulation)
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
        
        print("\n❌ All advanced methods failed")
        print("💡 The protection is very strong. Consider:")
        print("1. Try a different US VPN server (East Coast)")
        print("2. Use a residential proxy service")
        print("3. Try accessing from a different US location")
        print("4. Wait and try again later")
        return None

def main():
    """
    Main function to try all advanced bypass methods
    """
    print("🔬 ADVANCED BYPASS TECHNIQUES")
    print("=" * 60)
    
    bypass = AdvancedBypass()
    result = bypass.run_all_methods()
    
    if result:
        print("\n🎉 SUCCESS! One of the advanced methods worked!")
        print("You can now use this method for your scraping.")
    else:
        print("\n💡 All advanced methods failed.")
        print("The Incapsula protection is very sophisticated.")
        print("Consider trying a different US VPN server or paid proxy service.")

if __name__ == "__main__":
    main()
