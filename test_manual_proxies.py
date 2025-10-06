#!/usr/bin/env python3
"""
Test the specific proxy IPs you found manually
"""

import requests
import time

def test_single_proxy(ip, port):
    """
    Test a single proxy
    """
    proxy = f"{ip}:{port}"
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        print(f"Testing {proxy}...")
        
        # Test basic connectivity
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=15)
        if response.status_code == 200:
            ip_info = response.json()
            origin_ip = ip_info.get('origin', '')
            print(f"✓ {proxy} working! IP: {origin_ip}")
            
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
    # The specific IPs you found (without ports - we'll try common ports)
    proxy_ips = [
        "108.162.198.170",
        "103.116.7.55", 
        "108.162.198.13",
        "108.162.198.162",
        "103.116.7.1",
        "104.238.68.15",
        "104.238.68.6",
        "103.116.7.54",
        "108.162.198.166",
        "108.162.198.121",
        "103.116.7.114",
        "108.162.198.117",
        "103.116.7.2",
        "103.116.7.132",
        "108.162.198.139"
    ]
    
    # Common proxy ports to try
    common_ports = ["8080", "3128", "80", "1080", "8888", "3129", "8081", "8000"]
    
    print("Testing the specific US proxy IPs you found...")
    print("=" * 60)
    
    working_proxies = []
    
    for ip in proxy_ips:
        print(f"\nTesting IP: {ip}")
        for port in common_ports:
            proxy = test_single_proxy(ip, port)
            if proxy:
                working_proxies.append(proxy)
                print(f"  ✓ Found working port {port} for {ip}")
                break  # Found working port for this IP
            time.sleep(1)  # Be respectful between tests
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
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
        print("No working US proxies found from your list")
        print("These IPs might be behind a firewall or not accessible")
        print("Try using a VPN with US location instead")

if __name__ == "__main__":
    main()
