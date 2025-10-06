#!/usr/bin/env python3
"""
Test fresh US proxies against SC Courts website
"""

import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class FreshProxyTester:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.working_proxies = []
        self.failed_proxies = []
        
        # Parse the proxy list
        self.proxy_list = self.parse_proxy_list()
        
    def parse_proxy_list(self):
        """
        Parse the provided proxy list
        """
        proxy_data = """104.233.26.241	6079	US	United States	transparent	no	no	31 mins ago
104.168.118.123	6079	US	United States	transparent	no	no	31 mins ago
38.154.206.37	9528	US	United States	transparent	no	no	31 mins ago
216.26.232.28	3129	US	United States	transparent	no	no	31 mins ago
181.214.13.236	6077	US	United States	transparent	no	no	31 mins ago
89.32.200.162	6618	LT	Lithuania	transparent	no	no	31 mins ago
23.95.244.226	6179	US	United States	transparent	no	no	31 mins ago
82.23.206.97	5903	US	United States	transparent	no	no	31 mins ago
136.0.189.89	6816	US	United States	transparent	no	no	31 mins ago
82.23.206.248	6054	US	United States	transparent	no	no	31 mins ago
184.174.58.36	5598	US	United States	transparent	no	no	31 mins ago
31.59.18.9	6590	US	United States	transparent	no	no	31 mins ago
198.46.202.109	5389	US	United States	transparent	no	no	31 mins ago
45.61.100.137	6405	US	United States	transparent	no	no	31 mins ago
142.111.150.130	6337	US	United States	transparent	no	no	31 mins ago
161.123.151.87	6071	US	United States	transparent	no	no	31 mins ago
161.123.154.16	6546	US	United States	transparent	no	no	31 mins ago
69.58.12.67	8072	US	United States	transparent	no	no	31 mins ago
142.147.129.138	5747	US	United States	transparent	no	no	31 mins ago
140.235.169.41	8085	US	United States	transparent	no	no	31 mins ago
104.233.12.190	6741	US	United States	transparent	no	no	31 mins ago
181.214.13.237	6078	US	United States	transparent	no	no	31 mins ago
45.41.171.25	6061	US	United States	transparent	no	no	31 mins ago
193.233.217.91	8085	US	United States	transparent	no	no	31 mins ago
192.241.125.192	8236	US	United States	transparent	no	no	31 mins ago
149.57.85.247	6215	US	United States	transparent	no	no	31 mins ago
104.239.106.164	5809	US	United States	transparent	no	no	31 mins ago
139.5.155.245	57412	ID	Indonesia	transparent	no	no	31 mins ago
140.235.170.156	8085	US	United States	transparent	no	no	31 mins ago
45.41.173.229	6596	US	United States	transparent	no	no	31 mins ago
104.238.10.253	6199	US	United States	transparent	no	no	31 mins ago
154.6.126.82	6053	SE	Sweden	transparent	no	no	31 mins ago
142.111.150.232	6439	US	United States	transparent	no	no	31 mins ago
184.174.24.86	6662	US	United States	transparent	no	no	31 mins ago
38.170.161.65	9116	US	United States	transparent	no	no	31 mins ago
136.0.194.253	6990	US	United States	transparent	no	no	31 mins ago
193.233.219.175	8085	US	United States	transparent	no	no	31 mins ago
192.198.117.242	7835	US	United States	transparent	no	no	31 mins ago
38.154.217.191	7382	US	United States	transparent	no	no	31 mins ago
45.81.149.137	6569	CA	Canada	transparent	no	no	31 mins ago
142.147.240.85	6607	US	United States	transparent	no	no	31 mins ago
38.170.172.127	5128	US	United States	transparent	no	no	31 mins ago
92.113.7.13	6739	US	United States	transparent	no	no	31 mins ago
45.56.174.94	6347	US	United States	transparent	no	no	31 mins ago
31.58.16.206	6173	US	United States	transparent	no	no	31 mins ago
193.142.36.97	8085	US	United States	transparent	no	no	31 mins ago
173.211.8.234	6346	US	United States	transparent	no	no	31 mins ago
216.74.118.48	6203	US	United States	transparent	no	no	31 mins ago
31.59.18.70	6651	US	United States	transparent	no	no	31 mins ago
38.170.173.253	7804	US	United States	transparent	no	no	31 mins ago
136.0.118.130	6502	US	United States	transparent	no	no	31 mins ago
142.111.58.200	6778	US	United States	transparent	no	no	31 mins ago
142.111.93.67	6628	US	United States	transparent	no	no	31 mins ago
145.223.56.77	7129	US	United States	transparent	no	no	31 mins ago
142.147.240.140	6662	US	United States	transparent	no	no	31 mins ago
91.198.95.164	5686	US	United States	transparent	no	no	31 mins ago
45.147.11.151	8085	US	United States	transparent	no	no	31 mins ago
82.26.218.187	6495	US	United States	transparent	no	no	31 mins ago"""
        
        proxies = []
        for line in proxy_data.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 4:
                ip = parts[0]
                port = parts[1]
                country = parts[2]
                country_name = parts[3]
                
                # Only include US proxies
                if country == 'US':
                    proxies.append({
                        'ip': ip,
                        'port': port,
                        'country': country,
                        'country_name': country_name,
                        'proxy_string': f"{ip}:{port}"
                    })
        
        print(f"📊 Found {len(proxies)} US proxies from the list")
        return proxies
    
    def test_proxy(self, proxy_info):
        """
        Test a single proxy
        """
        proxy_string = proxy_info['proxy_string']
        ip = proxy_info['ip']
        port = proxy_info['port']
        
        try:
            # Test basic connectivity first
            test_url = "http://httpbin.org/ip"
            proxy_dict = {
                'http': f'http://{proxy_string}',
                'https': f'http://{proxy_string}'
            }
            
            # Test with shorter timeout first
            response = requests.get(test_url, proxies=proxy_dict, timeout=10)
            
            if response.status_code == 200:
                # Check if we're getting the proxy IP
                proxy_ip = response.json().get('origin', '')
                if proxy_ip == ip:
                    print(f"✅ {proxy_string} - Basic connectivity OK")
                    
                    # Now test the target website
                    target_response = requests.get(
                        self.target_url, 
                        proxies=proxy_dict, 
                        timeout=30,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                    )
                    
                    if target_response.status_code == 200:
                        if 'Incapsula' in target_response.text:
                            print(f"⚠️ {proxy_string} - Incapsula protection detected")
                            return {'proxy': proxy_string, 'status': 'incapsula', 'ip': ip}
                        else:
                            print(f"🎉 {proxy_string} - SUCCESS! No protection detected!")
                            return {'proxy': proxy_string, 'status': 'success', 'ip': ip}
                    elif target_response.status_code == 403:
                        print(f"❌ {proxy_string} - 403 Forbidden (blocked)")
                        return {'proxy': proxy_string, 'status': 'blocked', 'ip': ip}
                    else:
                        print(f"❌ {proxy_string} - Status {target_response.status_code}")
                        return {'proxy': proxy_string, 'status': 'error', 'ip': ip}
                else:
                    print(f"⚠️ {proxy_string} - IP mismatch (got {proxy_ip}, expected {ip})")
                    return {'proxy': proxy_string, 'status': 'ip_mismatch', 'ip': ip}
            else:
                print(f"❌ {proxy_string} - Basic connectivity failed")
                return {'proxy': proxy_string, 'status': 'connectivity_failed', 'ip': ip}
                
        except requests.exceptions.Timeout:
            print(f"⏰ {proxy_string} - Timeout")
            return {'proxy': proxy_string, 'status': 'timeout', 'ip': ip}
        except requests.exceptions.ConnectionError:
            print(f"🔌 {proxy_string} - Connection error")
            return {'proxy': proxy_string, 'status': 'connection_error', 'ip': ip}
        except Exception as e:
            print(f"❌ {proxy_string} - Error: {str(e)[:50]}")
            return {'proxy': proxy_string, 'status': 'error', 'ip': ip}
    
    def test_proxies_parallel(self, max_workers=10):
        """
        Test proxies in parallel
        """
        print(f"🧪 Testing {len(self.proxy_list)} US proxies...")
        print("=" * 60)
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in self.proxy_list
            }
            
            # Process results as they complete
            for future in as_completed(future_to_proxy):
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Show progress
                    completed = len(results)
                    total = len(self.proxy_list)
                    print(f"Progress: {completed}/{total} ({completed/total*100:.1f}%)")
                    
                except Exception as e:
                    print(f"❌ Error processing result: {e}")
        
        return results
    
    def analyze_results(self, results):
        """
        Analyze test results
        """
        print("\n📊 RESULTS ANALYSIS")
        print("=" * 60)
        
        success_proxies = [r for r in results if r['status'] == 'success']
        incapsula_proxies = [r for r in results if r['status'] == 'incapsula']
        blocked_proxies = [r for r in results if r['status'] == 'blocked']
        error_proxies = [r for r in results if r['status'] in ['error', 'timeout', 'connection_error']]
        
        print(f"✅ SUCCESS: {len(success_proxies)} proxies")
        print(f"⚠️ INCAPSULA: {len(incapsula_proxies)} proxies")
        print(f"❌ BLOCKED: {len(blocked_proxies)} proxies")
        print(f"🔌 ERRORS: {len(error_proxies)} proxies")
        
        if success_proxies:
            print("\n🎉 WORKING PROXIES:")
            for proxy in success_proxies:
                print(f"  ✅ {proxy['proxy']} (IP: {proxy['ip']})")
            
            # Save working proxies
            with open('working_proxies.txt', 'w') as f:
                for proxy in success_proxies:
                    f.write(f"{proxy['proxy']}\n")
            print(f"\n💾 Saved {len(success_proxies)} working proxies to working_proxies.txt")
        
        if incapsula_proxies:
            print("\n⚠️ INCAPSULA PROTECTION (but working):")
            for proxy in incapsula_proxies:
                print(f"  ⚠️ {proxy['proxy']} (IP: {proxy['ip']})")
        
        return success_proxies, incapsula_proxies
    
    def create_scraper_with_proxy(self, proxy_string):
        """
        Create a scraper script that uses the working proxy
        """
        scraper_content = f'''#!/usr/bin/env python3
"""
SC Courts scraper with working proxy: {proxy_string}
"""

import requests
import time
from bs4 import BeautifulSoup

class SCCourtsScraperWithProxy:
    def __init__(self, proxy_string):
        self.proxy_string = proxy_string
        self.proxy_dict = {{
            'http': f'http://{{proxy_string}}',
            'https': f'http://{{proxy_string}}'
        }}
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
        self.session = requests.Session()
        self.session.proxies.update(self.proxy_dict)
        
        self.headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }}
    
    def scrape(self):
        """
        Scrape the SC Courts website
        """
        try:
            print(f"🌐 Using proxy: {{self.proxy_string}}")
            print(f"🎯 Target: {{self.target_url}}")
            
            # Make request
            response = self.session.get(self.target_url, headers=self.headers, timeout=30)
            
            print(f"📊 Status: {{response.status_code}}")
            
            if response.status_code == 200:
                if 'Incapsula' in response.text:
                    print("⚠️ Incapsula protection detected")
                    return False
                else:
                    print("✅ SUCCESS! No protection detected")
                    
                    # Parse the response
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Save response for inspection
                    with open('response_with_proxy.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    print("💾 Response saved to response_with_proxy.html")
                    
                    # Extract useful information
                    forms = soup.find_all('form')
                    inputs = soup.find_all('input')
                    selects = soup.find_all('select')
                    links = soup.find_all('a')
                    scripts = soup.find_all('script')
                    
                    print(f"📋 Found:")
                    print(f"  - Forms: {{len(forms)}}")
                    print(f"  - Inputs: {{len(inputs)}}")
                    print(f"  - Selects: {{len(selects)}}")
                    print(f"  - Links: {{len(links)}}")
                    print(f"  - Scripts: {{len(scripts)}}")
                    
                    return True
            else:
                print(f"❌ Failed with status: {{response.status_code}}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {{e}}")
            return False

def main():
    scraper = SCCourtsScraperWithProxy("{proxy_string}")
    success = scraper.scrape()
    
    if success:
        print("\\n🎉 SUCCESS! You can now scrape the website!")
    else:
        print("\\n❌ Failed to scrape the website")

if __name__ == "__main__":
    main()
'''
        
        with open('scraper_with_proxy.py', 'w') as f:
            f.write(scraper_content)
        
        print(f"📝 Created scraper_with_proxy.py using proxy: {proxy_string}")

def main():
    """
    Main function
    """
    print("🧪 FRESH PROXY TESTER")
    print("=" * 60)
    
    tester = FreshProxyTester()
    
    # Test proxies in parallel
    results = tester.test_proxies_parallel(max_workers=15)
    
    # Analyze results
    success_proxies, incapsula_proxies = tester.analyze_results(results)
    
    if success_proxies:
        # Create scraper with the first working proxy
        best_proxy = success_proxies[0]['proxy']
        tester.create_scraper_with_proxy(best_proxy)
        
        print(f"\n🎉 SUCCESS! Found {len(success_proxies)} working proxies!")
        print(f"💡 Use the scraper: python scraper_with_proxy.py")
    elif incapsula_proxies:
        print(f"\n⚠️ Found {len(incapsula_proxies)} proxies with Incapsula protection")
        print("💡 These might work with additional bypass techniques")
    else:
        print("\n❌ No working proxies found")
        print("💡 Try different proxy sources or VPN")

if __name__ == "__main__":
    main()
