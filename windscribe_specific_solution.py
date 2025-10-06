#!/usr/bin/env python3
"""
Specific solutions for Windscribe VPN users
"""

import requests
import time
import random
from bs4 import BeautifulSoup

class WindscribeSpecificSolution:
    def __init__(self):
        self.session = requests.Session()
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def check_current_status(self):
        """
        Check current connection status
        """
        print("🔍 Checking current connection status...")
        
        try:
            # Check IP and location
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                your_ip = ip_info.get('origin', '')
                print(f"📍 Your IP: {your_ip}")
                
                # Get location
                geo_response = requests.get(f'http://ip-api.com/json/{your_ip}', timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    isp = geo_data.get('isp', 'Unknown')
                    
                    print(f"🌍 Location: {city}, {region}, {country}")
                    print(f"🏢 ISP: {isp}")
                    
                    if country == 'United States':
                        print("✅ You're connected from the US")
                        return True
                    else:
                        print(f"❌ You're connected from {country}, not US")
                        return False
                else:
                    print("⚠️ Could not determine location")
                    return None
            else:
                print("❌ Could not get IP information")
                return None
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            return None
    
    def try_different_windscribe_servers(self):
        """
        Try different Windscribe US servers
        """
        print("🔄 Trying different Windscribe US servers...")
        print("💡 Switch to these servers in Windscribe app:")
        
        recommended_servers = [
            "US East - New York",
            "US East - Washington DC", 
            "US East - Miami",
            "US East - Atlanta",
            "US West - Los Angeles",
            "US West - San Francisco",
            "US Central - Chicago",
            "US Central - Dallas"
        ]
        
        for i, server in enumerate(recommended_servers, 1):
            print(f"\n{i}. {server}")
            print("   - Switch to this server in Windscribe")
            print("   - Wait 30 seconds for connection")
            print("   - Then run: python windscribe_specific_solution.py")
            print("   - Check if it works")
        
        return None
    
    def test_current_server(self):
        """
        Test the current Windscribe server
        """
        print("🧪 Testing current Windscribe server...")
        
        try:
            response = requests.get(self.target_url, timeout=30)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                if 'Incapsula' in response.text:
                    print("❌ Still getting Incapsula protection page")
                    print("💡 Try a different US server in Windscribe")
                    return False
                else:
                    print("✅ SUCCESS! No Incapsula protection detected!")
                    print("🎉 You can now scrape the website!")
                    return True
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing server: {e}")
            return False
    
    def windscribe_specific_headers(self):
        """
        Try Windscribe-specific headers
        """
        print("🔧 Trying Windscribe-specific headers...")
        
        # Headers that might work better with Windscribe
        headers = {
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
            # Try with different request patterns
            print("  Trying direct request...")
            response1 = requests.get(self.target_url, headers=headers, timeout=30)
            
            if response1.status_code == 200 and 'Incapsula' not in response1.text:
                print("  ✅ SUCCESS with direct request!")
                return response1
            
            print("  Trying with session...")
            response2 = self.session.get(self.target_url, headers=headers, timeout=30)
            
            if response2.status_code == 200 and 'Incapsula' not in response2.text:
                print("  ✅ SUCCESS with session!")
                return response2
            
            print("  ❌ Still blocked with Windscribe-specific headers")
            return None
            
        except Exception as e:
            print(f"  ❌ Error with Windscribe-specific headers: {e}")
            return None
    
    def windscribe_troubleshooting(self):
        """
        Windscribe-specific troubleshooting
        """
        print("🔧 WINDSCRIBE TROUBLESHOOTING")
        print("=" * 40)
        
        print("1. 📍 Check your current server:")
        print("   - Open Windscribe app")
        print("   - Check which US server you're connected to")
        print("   - Try switching to a different US server")
        
        print("\n2. 🔄 Try these specific servers:")
        print("   - US East - New York (recommended)")
        print("   - US East - Washington DC")
        print("   - US East - Miami")
        print("   - US West - Los Angeles")
        
        print("\n3. ⚙️ Windscribe settings to try:")
        print("   - Enable 'Firewall' in Windscribe settings")
        print("   - Try 'Stealth' mode if available")
        print("   - Disable 'Kill Switch' temporarily")
        
        print("\n4. 🌐 Try different protocols:")
        print("   - Switch between UDP and TCP")
        print("   - Try different ports if available")
        
        print("\n5. ⏰ Timing:")
        print("   - Try different times of day")
        print("   - Some servers might be less blocked at certain times")
        
        print("\n6. 🔄 Restart sequence:")
        print("   - Disconnect from Windscribe")
        print("   - Wait 30 seconds")
        print("   - Connect to different US server")
        print("   - Wait 30 seconds")
        print("   - Test again")
    
    def run_windscribe_solution(self):
        """
        Run Windscribe-specific solution
        """
        print("🔐 WINDSCRIBE VPN SPECIFIC SOLUTION")
        print("=" * 50)
        
        # Check current status
        is_us = self.check_current_status()
        
        if not is_us:
            print("\n❌ You're not connected from the US")
            print("💡 Please connect to a US server in Windscribe")
            return None
        
        # Test current server
        print("\n🧪 Testing current server...")
        if self.test_current_server():
            print("🎉 SUCCESS! Your current server works!")
            return True
        
        # Try Windscribe-specific headers
        print("\n🔧 Trying Windscribe-specific headers...")
        result = self.windscribe_specific_headers()
        if result:
            print("🎉 SUCCESS with Windscribe-specific headers!")
            return result
        
        # Show troubleshooting
        print("\n❌ Current server still blocked")
        self.windscribe_troubleshooting()
        
        return None

def main():
    """
    Main function for Windscribe users
    """
    print("🔐 WINDSCRIBE VPN SOLUTION")
    print("=" * 40)
    
    solution = WindscribeSpecificSolution()
    result = solution.run_windscribe_solution()
    
    if result:
        print("\n🎉 SUCCESS! Windscribe is working!")
        print("You can now run: python sc_courts_scraper_enhanced.py")
    else:
        print("\n💡 Try these steps:")
        print("1. Switch to US East - New York server")
        print("2. Wait 30 seconds")
        print("3. Run this script again")
        print("4. If still blocked, try US East - Washington DC")

if __name__ == "__main__":
    main()
