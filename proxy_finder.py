#!/usr/bin/env python3
"""
Proxy Finder for US-based proxies
Helps find working US proxies for scraping
"""

import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class USProxyFinder:
    def __init__(self):
        self.working_proxies = []
        
    def get_free_proxies(self):
        """
        Get free proxy lists from various sources
        """
        proxy_sources = [
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=US&format=json",
        ]
        
        proxies = []
        
        for source in proxy_sources:
            try:
                logger.info(f"Fetching proxies from: {source}")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    if "json" in source:
                        data = response.json()
                        for proxy_data in data:
                            if isinstance(proxy_data, dict) and 'ip' in proxy_data:
                                proxies.append(f"{proxy_data['ip']}:{proxy_data['port']}")
                            else:
                                proxies.append(proxy_data)
                    else:
                        # Plain text format
                        for line in response.text.strip().split('\n'):
                            if ':' in line:
                                proxies.append(line.strip())
                time.sleep(1)  # Be respectful
            except Exception as e:
                logger.warning(f"Failed to fetch from {source}: {e}")
        
        return list(set(proxies))  # Remove duplicates
    
    def test_proxy(self, proxy):
        """
        Test if a proxy is working and returns US IP
        """
        try:
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            # Test with httpbin to get IP info
            response = requests.get(
                'http://httpbin.org/ip', 
                proxies=proxy_dict, 
                timeout=10
            )
            
            if response.status_code == 200:
                ip_info = response.json()
                origin_ip = ip_info.get('origin', '')
                
                # Try to get country info
                try:
                    geo_response = requests.get(f'http://ip-api.com/json/{origin_ip}', timeout=5)
                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        country = geo_data.get('country', '')
                        if country == 'United States':
                            logger.info(f"Found US proxy: {proxy} (IP: {origin_ip})")
                            return proxy
                        else:
                            logger.info(f"Proxy {proxy} is from {country}, not US")
                    else:
                        logger.info(f"Proxy {proxy} works but couldn't verify country")
                        return proxy  # Assume it's good if we can't verify
                except:
                    logger.info(f"Proxy {proxy} works but couldn't verify country")
                    return proxy  # Assume it's good if we can't verify
                    
        except Exception as e:
            logger.debug(f"Proxy {proxy} failed: {e}")
        
        return None
    
    def find_working_proxies(self, max_proxies=5):
        """
        Find working US proxies
        """
        logger.info("Fetching proxy lists...")
        all_proxies = self.get_free_proxies()
        logger.info(f"Found {len(all_proxies)} potential proxies")
        
        if not all_proxies:
            logger.warning("No proxies found from free sources")
            return []
        
        # Test proxies in parallel
        working_proxies = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in all_proxies[:50]}  # Test first 50
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result()
                    if result:
                        working_proxies.append(result)
                        if len(working_proxies) >= max_proxies:
                            break
                except Exception as e:
                    logger.debug(f"Error testing proxy {proxy}: {e}")
        
        logger.info(f"Found {len(working_proxies)} working US proxies")
        return working_proxies

def main():
    """
    Main function to find working US proxies
    """
    finder = USProxyFinder()
    proxies = finder.find_working_proxies()
    
    if proxies:
        print("\nWorking US Proxies:")
        for proxy in proxies:
            print(f"  {proxy}")
        
        # Save to file
        with open('us_proxies.txt', 'w') as f:
            for proxy in proxies:
                f.write(f"{proxy}\n")
        print(f"\nProxies saved to us_proxies.txt")
    else:
        print("No working US proxies found")

if __name__ == "__main__":
    main()
