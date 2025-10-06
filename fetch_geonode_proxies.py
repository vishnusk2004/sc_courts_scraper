#!/usr/bin/env python3
"""
Fetch US proxies from GeoNode API and test them
"""

import requests
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import json

def test_proxy(proxy_data):
    """
    Test if a proxy is working and US-based
    """
    ip = proxy_data['ip']
    port = proxy_data['port']
    country = proxy_data.get('country', '')
    
    # Only test US proxies
    if country != 'US':
        return None
    
    proxy = f"{ip}:{port}"
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        print(f"Testing {proxy} ({country})...")
        
        # Test basic connectivity
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=15)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            print(f"✓ {proxy} working! IP: {origin_ip}")
            
            # Get location info to double-check
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    actual_country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    
                    print(f"  Location: {city}, {region}, {actual_country}")
                    
                    if actual_country == 'United States':
                        print(f"  ✓ {proxy} is confirmed US-based - PERFECT!")
                        return proxy
                    else:
                        print(f"  ⚠ {proxy} is actually in {actual_country}, not US")
                        return None
                else:
                    print(f"  ✓ {proxy} - Working (location verification failed)")
                    return proxy  # Assume it's good if we can't verify
            except Exception as e:
                print(f"  ✓ {proxy} - Working (location check failed: {e})")
                return proxy  # Assume it's good if we can't verify
        else:
            print(f"✗ {proxy} failed with status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ {proxy} failed: {e}")
        return None

def fetch_geonode_proxies():
    """
    Fetch proxies from GeoNode API and test US ones
    """
    api_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
    
    print("Fetching proxies from GeoNode API...")
    print(f"API URL: {api_url}")
    
    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            proxies = data.get('data', [])
            print(f"Found {len(proxies)} total proxies from API")
            
            # Filter for US proxies only
            us_proxies = [p for p in proxies if p.get('country') == 'US']
            print(f"Found {len(us_proxies)} US proxies")
            
            if not us_proxies:
                print("No US proxies found in this batch")
                return []
            
            # Test US proxies in parallel
            working_proxies = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in us_proxies[:20]}  # Test first 20 US proxies
                
                for future in concurrent.futures.as_completed(future_to_proxy):
                    proxy_data = future_to_proxy[future]
                    try:
                        result = future.result()
                        if result:
                            working_proxies.append(result)
                    except Exception as e:
                        print(f"Error testing proxy: {e}")
            
            if working_proxies:
                print(f"\nFound {len(working_proxies)} working US proxies:")
                for proxy in working_proxies:
                    print(f"  {proxy}")
                
                # Save to file
                with open('us_proxies.txt', 'w') as f:
                    for proxy in working_proxies:
                        f.write(f"{proxy}\n")
                print(f"\nProxies saved to us_proxies.txt")
                print("You can now run: python sc_courts_scraper.py --proxy")
            else:
                print("No working US proxies found from GeoNode API")
        else:
            print(f"Failed to fetch proxies from API: {response.status_code}")
    except Exception as e:
        print(f"Error fetching proxies: {e}")

if __name__ == "__main__":
    fetch_geonode_proxies()
