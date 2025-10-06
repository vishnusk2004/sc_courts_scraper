#!/usr/bin/env python3
"""
Comprehensive proxy finder that tries multiple sources
"""

import requests
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import json
import random

class ComprehensiveProxyFinder:
    def __init__(self):
        self.working_proxies = []
        
    def fetch_geonode_proxies(self):
        """
        Fetch proxies from GeoNode API
        """
        try:
            print("Fetching from GeoNode API...")
            url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                proxies = data.get('data', [])
                us_proxies = [p for p in proxies if p.get('country') == 'US']
                print(f"Found {len(us_proxies)} US proxies from GeoNode")
                return us_proxies
        except Exception as e:
            print(f"GeoNode API failed: {e}")
        return []
    
    def fetch_proxyscrape_proxies(self):
        """
        Fetch proxies from ProxyScrape API
        """
        try:
            print("Fetching from ProxyScrape API...")
            url = "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=US&format=json"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Found {len(data)} US proxies from ProxyScrape")
                return data
        except Exception as e:
            print(f"ProxyScrape API failed: {e}")
        return []
    
    def test_proxy(self, proxy_data):
        """
        Test if a proxy is working
        """
        if isinstance(proxy_data, dict):
            ip = proxy_data.get('ip', '')
            port = proxy_data.get('port', '')
        else:
            # Handle string format
            if ':' in str(proxy_data):
                ip, port = str(proxy_data).split(':', 1)
            else:
                return None
        
        proxy = f"{ip}:{port}"
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        try:
            # Test with a simple request
            response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                origin_ip = ip_info.get('origin', '')
                
                # Quick location check
                try:
                    geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=5)
                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        country = geo_data.get('country', '')
                        if country == 'United States':
                            print(f"✓ {proxy} - Working US proxy!")
                            return proxy
                        else:
                            print(f"⚠ {proxy} - Not US ({country})")
                            return None
                except:
                    print(f"✓ {proxy} - Working (location unknown)")
                    return proxy
        except Exception as e:
            print(f"✗ {proxy} - Failed: {str(e)[:50]}...")
            return None
    
    def find_working_proxies(self):
        """
        Find working US proxies from multiple sources
        """
        all_proxies = []
        
        # Try multiple sources
        sources = [
            self.fetch_geonode_proxies,
            self.fetch_proxyscrape_proxies,
        ]
        
        for source_func in sources:
            try:
                proxies = source_func()
                all_proxies.extend(proxies)
            except Exception as e:
                print(f"Source failed: {e}")
        
        if not all_proxies:
            print("No proxies found from any source")
            return []
        
        print(f"\nTesting {len(all_proxies)} proxies...")
        
        # Test proxies in parallel
        working_proxies = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in all_proxies[:30]}  # Test first 30
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                try:
                    result = future.result()
                    if result:
                        working_proxies.append(result)
                        if len(working_proxies) >= 5:  # Stop after finding 5 working proxies
                            break
                except Exception as e:
                    print(f"Error testing proxy: {e}")
        
        return working_proxies

def main():
    """
    Main function to find working US proxies
    """
    print("Comprehensive US Proxy Finder")
    print("=" * 40)
    
    finder = ComprehensiveProxyFinder()
    working_proxies = finder.find_working_proxies()
    
    if working_proxies:
        print(f"\n🎉 Found {len(working_proxies)} working US proxies:")
        for proxy in working_proxies:
            print(f"  {proxy}")
        
        # Save to file
        with open('us_proxies.txt', 'w') as f:
            for proxy in working_proxies:
                f.write(f"{proxy}\n")
        print(f"\nProxies saved to us_proxies.txt")
        print("You can now run: python sc_courts_scraper.py --proxy")
    else:
        print("\n❌ No working US proxies found")
        print("\nAlternative solutions:")
        print("1. Use a US-based VPN (most reliable)")
        print("2. Try paid proxy services")
        print("3. Use a cloud server in the US")
        print("4. Try different proxy sources")

if __name__ == "__main__":
    main()
