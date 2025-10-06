#!/usr/bin/env python3
"""
Simple script to manually add US proxies
"""

import sys

def add_proxy():
    """
    Add a proxy to the us_proxies.txt file
    """
    if len(sys.argv) != 2:
        print("Usage: python add_proxy.py <proxy_ip:port>")
        print("Example: python add_proxy.py 192.168.1.1:8080")
        return
    
    proxy = sys.argv[1]
    
    # Validate format
    if ':' not in proxy:
        print("Error: Proxy must be in format 'ip:port'")
        return
    
    try:
        # Add to file
        with open('us_proxies.txt', 'a') as f:
            f.write(f"{proxy}\n")
        print(f"Added proxy: {proxy}")
        print("You can now run: python sc_courts_scraper.py --proxy")
    except Exception as e:
        print(f"Error adding proxy: {e}")

if __name__ == "__main__":
    add_proxy()
