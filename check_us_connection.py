#!/usr/bin/env python3
"""
Check if your current connection appears to be US-based
"""

import requests
import json

def check_connection():
    """
    Check if the current connection is US-based
    """
    try:
        print("Checking your current connection...")
        
        # Get IP info
        response = requests.get('http://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            print(f"Your IP: {origin_ip}")
            
            # Get location info
            geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=10)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                country = geo_data.get('country', 'Unknown')
                region = geo_data.get('regionName', 'Unknown')
                city = geo_data.get('city', 'Unknown')
                isp = geo_data.get('isp', 'Unknown')
                
                print(f"Location: {city}, {region}, {country}")
                print(f"ISP: {isp}")
                
                if country == 'United States':
                    print("✅ You appear to be connected from the US!")
                    print("You should be able to access the SC courts website.")
                    return True
                else:
                    print("❌ You are NOT connected from the US")
                    print("You need a US-based VPN or proxy to access the website.")
                    return False
            else:
                print("⚠ Could not determine location")
                return None
        else:
            print("❌ Could not get IP information")
            return None
            
    except Exception as e:
        print(f"❌ Error checking connection: {e}")
        return None

def main():
    print("US Connection Checker")
    print("=" * 30)
    
    is_us = check_connection()
    
    if is_us:
        print("\n🎉 You can now try running the scraper:")
        print("python sc_courts_scraper.py")
    elif is_us is False:
        print("\n💡 To access the SC courts website, you need:")
        print("1. A US-based VPN (recommended)")
        print("2. A US-based proxy")
        print("3. A cloud server in the US")
        print("\nPopular US VPN services:")
        print("- ExpressVPN")
        print("- NordVPN") 
        print("- Surfshark")
        print("- CyberGhost")
    else:
        print("\n⚠ Could not determine your location")
        print("Try running the scraper anyway: python sc_courts_scraper.py")

if __name__ == "__main__":
    main()
