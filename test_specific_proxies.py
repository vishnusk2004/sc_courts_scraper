#!/usr/bin/env python3
"""
Test the specific US proxies you found
"""

import requests
import time
import concurrent.futures
from threading import ThreadPoolExecutor

def test_proxy(proxy_ip, proxy_port):
    """
    Test a specific proxy
    """
    proxy = f"{proxy_ip}:{proxy_port}"
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        print(f"Testing {proxy}...")
        
        # Test basic connectivity
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = response.json().get('origin', '')
            print(f"✓ {proxy} working! IP: {origin_ip}")
            
            # Get location info
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=5)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    
                    print(f"  Location: {city}, {region}, {country}")
                    
                    if country == 'United States':
                        print(f"  ✓ {proxy} is US-based - PERFECT!")
                        return proxy
                    else:
                        print(f"  ⚠ {proxy} is in {country}, not US")
                        return None
                else:
                    print(f"  ⚠ Could not determine location for {proxy}")
                    return proxy  # Assume it's good if we can't verify
            except Exception as e:
                print(f"  ⚠ Could not get location info for {proxy}: {e}")
                return proxy  # Assume it's good if we can't verify
        else:
            print(f"✗ {proxy} failed with status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ {proxy} failed: {e}")
        return None

def main():
    # The proxies you found
    proxies_to_test = [
        ("108.162.198.170", "8080"),  # Assuming port 8080, you may need to adjust
        ("103.116.7.55", "8080"),
        ("108.162.198.13", "8080"),
        ("108.162.198.162", "8080"),
        ("103.116.7.1", "8080"),
        ("104.238.68.15", "8080"),
        ("104.238.68.6", "8080"),
        ("103.116.7.54", "8080"),
        ("108.162.198.166", "8080"),
        ("108.162.198.121", "8080"),
        ("103.116.7.114", "8080"),
        ("108.162.198.117", "8080"),
        ("103.116.7.2", "8080"),
        ("103.116.7.132", "8080"),
        ("108.162.198.139", "8080"),
    ]
    
    # Common proxy ports to try
    common_ports = ["8080", "3128", "80", "1080", "8888", "3129"]
    
    print("Testing US proxies you found...")
    print("=" * 50)
    
    working_proxies = []
    
    # Test each proxy with different ports
    for proxy_ip, _ in proxies_to_test:
        for port in common_ports:
            proxy = test_proxy(proxy_ip, port)
            if proxy:
                working_proxies.append(proxy)
                break  # Found working port for this IP
            time.sleep(1)  # Be respectful
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    
    if working_proxies:
        print(f"Found {len(working_proxies)} working US proxies:")
        for proxy in working_proxies:
            print(f"  {proxy}")
        
        # Save to file
        with open('us_proxies.txt', 'w') as f:
            for proxy in working_proxies:
                f.write(f"{proxy}\n")
        print(f"\nProxies saved to us_proxies.txt")
        print("You can now run: python sc_courts_scraper.py --proxy")
    else:
        print("No working US proxies found from this list")
        print("You may need to try different ports or find other proxies")

if __name__ == "__main__":
    main()
