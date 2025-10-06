#!/usr/bin/env python3
"""
Test the authenticated proxies you found
"""

import requests
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def test_authenticated_proxy(proxy_line):
    """
    Test an authenticated proxy
    Format: ip:port:username:password
    """
    try:
        parts = proxy_line.strip().split(':')
        if len(parts) != 4:
            return None
            
        ip, port, username, password = parts
        
        # Create proxy URL with authentication
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        proxy_dict = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        print(f"Testing {ip}:{port}...")
        
        # Test basic connectivity
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=15)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            print(f"✓ {ip}:{port} working! IP: {origin_ip}")
            
            # Get location info
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    
                    print(f"  Location: {city}, {region}, {country}")
                    
                    if country == 'United States':
                        print(f"  ✓ {ip}:{port} is US-based - PERFECT!")
                        return f"{ip}:{port}"
                    else:
                        print(f"  ⚠ {ip}:{port} is in {country}, not US")
                        return None
                else:
                    print(f"  ✓ {ip}:{port} - Working (location unknown)")
                    return f"{ip}:{port}"
            except Exception as e:
                print(f"  ✓ {ip}:{port} - Working (location check failed: {e})")
                return f"{ip}:{port}"
        else:
            print(f"✗ {ip}:{port} failed with status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ {ip}:{port} failed: {e}")
        return None

def main():
    """
    Test the authenticated proxies you provided
    """
    # The proxy list you found
    proxy_list = [
        "45.43.190.72:6590:nxhkryfv:fre3i4dn5dvq",
        "64.137.49.92:6633:nxhkryfv:fre3i4dn5dvq",
        "104.238.9.181:6634:nxhkryfv:fre3i4dn5dvq",
        "154.92.116.177:6489:nxhkryfv:fre3i4dn5dvq",
        "185.213.242.108:8572:nxhkryfv:fre3i4dn5dvq",
        "91.212.100.78:6654:nxhkryfv:fre3i4dn5dvq",
        "104.239.41.106:6461:nxhkryfv:fre3i4dn5dvq",
        "45.43.185.178:6184:nxhkryfv:fre3i4dn5dvq",
        "107.152.214.117:8694:nxhkryfv:fre3i4dn5dvq",
        "198.20.191.145:7201:nxhkryfv:fre3i4dn5dvq",
        "45.41.179.206:6741:nxhkryfv:fre3i4dn5dvq",
        "154.92.126.109:5447:nxhkryfv:fre3i4dn5dvq",
        "209.127.143.148:8247:nxhkryfv:fre3i4dn5dvq",
        "104.239.81.23:6558:nxhkryfv:fre3i4dn5dvq",
        "216.74.118.242:6397:nxhkryfv:fre3i4dn5dvq",
        "45.12.150.160:6178:nxhkryfv:fre3i4dn5dvq",
        "77.83.233.99:6717:nxhkryfv:fre3i4dn5dvq",
        "45.61.123.23:5702:nxhkryfv:fre3i4dn5dvq",
        "64.137.89.59:6132:nxhkryfv:fre3i4dn5dvq",
        "192.186.151.188:8689:nxhkryfv:fre3i4dn5dvq"
    ]
    
    print("Testing Authenticated Proxies")
    print("=" * 40)
    print(f"Testing {len(proxy_list)} proxies...")
    
    working_proxies = []
    
    # Test proxies in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_proxy = {executor.submit(test_authenticated_proxy, proxy): proxy for proxy in proxy_list}
        
        for future in concurrent.futures.as_completed(future_to_proxy):
            try:
                result = future.result()
                if result:
                    working_proxies.append(result)
                    if len(working_proxies) >= 5:  # Stop after finding 5 working proxies
                        break
            except Exception as e:
                print(f"Error testing proxy: {e}")
    
    print("\n" + "=" * 40)
    print("RESULTS:")
    print("=" * 40)
    
    if working_proxies:
        print(f"Found {len(working_proxies)} working proxies:")
        for proxy in working_proxies:
            print(f"  {proxy}")
        
        # Save to file
        with open('working_proxies.txt', 'w') as f:
            for proxy in working_proxies:
                f.write(f"{proxy}\n")
        print(f"\nWorking proxies saved to working_proxies.txt")
        print("You can now use these with the scraper!")
    else:
        print("No working proxies found from this list")
        print("These proxies might be:")
        print("- Expired or inactive")
        print("- Blocked by your ISP")
        print("- Not US-based")
        print("- Require different authentication")

if __name__ == "__main__":
    main()
