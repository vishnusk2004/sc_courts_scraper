#!/usr/bin/env python3
"""
Test if a proxy is working and shows IP location
"""

import requests
import sys

def test_proxy(proxy):
    """
    Test a proxy and show IP information
    """
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        print(f"Testing proxy: {proxy}")
        
        # Test basic connectivity
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            print(f"✓ Proxy working! IP: {origin_ip}")
            
            # Get location info
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=5)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    
                    print(f"Location: {city}, {region}, {country}")
                    
                    if country == 'United States':
                        print("✓ This is a US proxy - should work with the scraper!")
                        return True
                    else:
                        print(f"⚠ This proxy is in {country}, not US")
                        return False
                else:
                    print("⚠ Could not determine location")
                    return True  # Assume it's good if we can't verify
            except Exception as e:
                print(f"⚠ Could not get location info: {e}")
                return True  # Assume it's good if we can't verify
        else:
            print(f"✗ Proxy failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Proxy test failed: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_proxy.py <proxy_ip:port>")
        print("Example: python test_proxy.py 192.168.1.1:8080")
        return
    
    proxy = sys.argv[1]
    success = test_proxy(proxy)
    
    if success:
        print("\nThis proxy can be added to us_proxies.txt")
        print(f"Run: python add_proxy.py {proxy}")
    else:
        print("\nThis proxy is not working or not US-based")

if __name__ == "__main__":
    main()
