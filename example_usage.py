#!/usr/bin/env python3
"""
Example usage of the SC Courts Scraper
"""

from sc_courts_scraper import SCCourtsScraper

def example_with_manual_proxy():
    """
    Example of using the scraper with a manually specified proxy
    """
    # Example US proxy (replace with actual working US proxy)
    proxy_list = [
        {'http': 'http://proxy.example.com:8080', 'https': 'http://proxy.example.com:8080'}
    ]
    
    # Create scraper with proxy
    scraper = SCCourtsScraper(use_proxy=True, proxy_list=proxy_list)
    
    # Run the scraper
    result = scraper.run()
    
    if result:
        print("Scraping successful!")
        print(f"Found {result['forms_count']} forms")
        print(f"Found {result['inputs_count']} input fields")
    else:
        print("Scraping failed - check if proxy is working")

def example_without_proxy():
    """
    Example of using the scraper without proxy (will likely fail due to geo-blocking)
    """
    scraper = SCCourtsScraper(use_proxy=False)
    result = scraper.run()
    
    if result:
        print("Scraping successful!")
    else:
        print("Scraping failed - likely due to geo-blocking")

if __name__ == "__main__":
    print("SC Courts Scraper Example")
    print("=" * 30)
    
    print("\n1. Trying without proxy (will likely fail):")
    example_without_proxy()
    
    print("\n2. To use with proxy, modify the proxy_list in example_with_manual_proxy()")
    print("   with actual working US proxies, then uncomment the line below:")
    # example_with_manual_proxy()
