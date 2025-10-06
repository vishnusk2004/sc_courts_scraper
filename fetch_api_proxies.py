#!/usr/bin/env python3
"""
Fetch US proxies from the API URL you found
"""

import requests
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def test_proxy(proxy):
    """
    Test if a proxy is working
    """
    # Clean up proxy format - remove http:// prefix if present
    if proxy.startswith('http://'):
        proxy = proxy[7:]  # Remove 'http://'
    
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            
            # Get location info
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=5)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    if country == 'United States':
                        print(f"✓ {proxy} - US proxy working!")
                        return proxy
                    else:
                        print(f"⚠ {proxy} - Not US ({country})")
                        return None
                else:
                    print(f"✓ {proxy} - Working (location unknown)")
                    return proxy
            except:
                print(f"✓ {proxy} - Working (location unknown)")
                return proxy
    except Exception as e:
        print(f"✗ {proxy} - Failed: {e}")
        return None

def fetch_and_test_proxies():
    """
    Fetch proxies from API and test them
    """
    api_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=us&proxy_format=protocolipport&format=text"
    
    print("Fetching US proxies from API...")
    print(f"API URL: {api_url}")
    
    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            proxies = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
            print(f"Found {len(proxies)} proxies from API")
            
            # Test proxies in parallel
            working_proxies = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies[:20]}  # Test first 20
                
                for future in concurrent.futures.as_completed(future_to_proxy):
                    proxy = future_to_proxy[future]
                    try:
                        result = future.result()
                        if result:
                            working_proxies.append(result)
                    except Exception as e:
                        print(f"Error testing {proxy}: {e}")
            
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
                print("No working US proxies found from API")
        else:
            print(f"Failed to fetch proxies from API: {response.status_code}")
    except Exception as e:
        print(f"Error fetching proxies: {e}")

if __name__ == "__main__":
    fetch_and_test_proxies()
