#!/usr/bin/env python3
"""
Test if you have a working US VPN connection
"""

import requests
import json
import time

def test_vpn_connection():
    """
    Test if your VPN connection is working and US-based
    """
    print("🔍 Testing VPN Connection...")
    print("=" * 40)
    
    try:
        # Get your current IP
        print("Getting your current IP...")
        response = requests.get('http://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            your_ip = ip_info.get('origin', '')
            print(f"📍 Your IP: {your_ip}")
            
            # Get detailed location info
            print("Getting location details...")
            geo_response = requests.get(f'http://ip-api.com/json/{your_ip}', timeout=10)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                country = geo_data.get('country', 'Unknown')
                region = geo_data.get('regionName', 'Unknown')
                city = geo_data.get('city', 'Unknown')
                isp = geo_data.get('isp', 'Unknown')
                timezone = geo_data.get('timezone', 'Unknown')
                
                print(f"🌍 Location: {city}, {region}, {country}")
                print(f"🏢 ISP: {isp}")
                print(f"⏰ Timezone: {timezone}")
                
                if country == 'United States':
                    print("\n✅ SUCCESS! You're connected from the US!")
                    print("🎉 You can now run the SC courts scraper!")
                    return True
                else:
                    print(f"\n❌ You're connected from {country}, not the US")
                    print("💡 You need a US-based VPN to access the SC courts website")
                    return False
            else:
                print("⚠️ Could not determine location")
                return None
        else:
            print("❌ Could not get IP information")
            return None
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return None

def test_sc_courts_access():
    """
    Test if you can access the SC courts website
    """
    print("\n🏛️ Testing SC Courts Website Access...")
    print("=" * 40)
    
    try:
        url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        print(f"Testing: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! You can access the SC courts website!")
            print("🎉 The scraper should work now!")
            return True
        elif response.status_code == 403:
            print("❌ 403 Forbidden - You're still blocked")
            print("💡 Try a different US VPN server")
            return False
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing SC courts website: {e}")
        return False

def main():
    """
    Main function to test VPN connection
    """
    print("🔐 VPN Connection Tester")
    print("=" * 50)
    
    # Test VPN connection
    is_us = test_vpn_connection()
    
    if is_us:
        # Test SC courts access
        can_access = test_sc_courts_access()
        
        if can_access:
            print("\n🎉 PERFECT! Everything is working!")
            print("You can now run: python sc_courts_scraper.py")
        else:
            print("\n⚠️ VPN is working but SC courts still blocked")
            print("Try a different US VPN server (East Coast recommended)")
    elif is_us is False:
        print("\n💡 To fix this:")
        print("1. Connect to a US VPN server")
        print("2. Try East Coast US servers")
        print("3. Make sure VPN is working properly")
        print("4. Run this test again")
    else:
        print("\n⚠️ Could not determine your location")
        print("Try running the scraper anyway: python sc_courts_scraper.py")

if __name__ == "__main__":
    main()
