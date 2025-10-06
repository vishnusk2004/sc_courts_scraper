#!/usr/bin/env python3
"""
Test the provided proxy list for SC Courts access
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProxyTester:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.proxies = []
        self.working_proxies = []
        
    def parse_proxy_list(self, proxy_text):
        """
        Parse the proxy list from the provided text
        """
        lines = proxy_text.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    ip = parts[0]
                    port = parts[1]
                    country = parts[2] if len(parts) > 2 else 'Unknown'
                    
                    # Only test US proxies
                    if country == 'US':
                        self.proxies.append({
                            'ip': ip,
                            'port': port,
                            'country': country,
                            'proxy': f"{ip}:{port}"
                        })
        
        print(f"📊 Found {len(self.proxies)} US proxies to test")
        return self.proxies
    
    def test_proxy(self, proxy_info):
        """
        Test a single proxy
        """
        proxy = proxy_info['proxy']
        ip = proxy_info['ip']
        port = proxy_info['port']
        
        try:
            # Test proxy with a simple request first
            test_url = "http://httpbin.org/ip"
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            # Test if proxy is working
            response = requests.get(test_url, proxies=proxy_dict, timeout=10)
            if response.status_code == 200:
                proxy_ip = response.json().get('origin', '')
                print(f"✅ Proxy {proxy} working - IP: {proxy_ip}")
                
                # Now test the target website
                try:
                    target_response = requests.get(
                        self.target_url, 
                        proxies=proxy_dict, 
                        timeout=30,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                    )
                    
                    if target_response.status_code == 200:
                        if 'Incapsula' in target_response.text:
                            print(f"⚠️ Proxy {proxy} - Incapsula protection")
                            return {'proxy': proxy, 'status': 'incapsula', 'ip': proxy_ip}
                        else:
                            print(f"🎉 SUCCESS! Proxy {proxy} - No protection!")
                            return {'proxy': proxy, 'status': 'success', 'ip': proxy_ip}
                    elif target_response.status_code == 403:
                        print(f"❌ Proxy {proxy} - 403 Forbidden")
                        return {'proxy': proxy, 'status': 'blocked', 'ip': proxy_ip}
                    else:
                        print(f"❌ Proxy {proxy} - Status {target_response.status_code}")
                        return {'proxy': proxy, 'status': 'error', 'ip': proxy_ip}
                        
                except Exception as e:
                    print(f"❌ Proxy {proxy} - Target error: {e}")
                    return {'proxy': proxy, 'status': 'error', 'ip': proxy_ip}
            else:
                print(f"❌ Proxy {proxy} - Not working")
                return {'proxy': proxy, 'status': 'not_working', 'ip': ''}
                
        except Exception as e:
            print(f"❌ Proxy {proxy} - Connection error: {e}")
            return {'proxy': proxy, 'status': 'error', 'ip': ''}
    
    def test_all_proxies(self, max_workers=5):
        """
        Test all proxies with threading
        """
        print(f"🧪 Testing {len(self.proxies)} proxies...")
        print("=" * 60)
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in self.proxies
            }
            
            # Process results as they complete
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result['status'] == 'success':
                        self.working_proxies.append(result)
                        print(f"🎉 FOUND WORKING PROXY: {result['proxy']}")
                        
                except Exception as e:
                    print(f"❌ Error testing {proxy['proxy']}: {e}")
        
        return results
    
    def save_working_proxies(self):
        """
        Save working proxies to file
        """
        if self.working_proxies:
            with open('working_proxies.txt', 'w') as f:
                for proxy in self.working_proxies:
                    f.write(f"{proxy['proxy']}\n")
            print(f"💾 Saved {len(self.working_proxies)} working proxies to working_proxies.txt")
        else:
            print("❌ No working proxies found")
    
    def create_scraper_with_proxy(self):
        """
        Create a scraper that uses the first working proxy
        """
        if self.working_proxies:
            working_proxy = self.working_proxies[0]
            print(f"🚀 Creating scraper with proxy: {working_proxy['proxy']}")
            
            scraper_code = f'''#!/usr/bin/env python3
"""
SC Courts Scraper with Working Proxy
"""

import requests
import time
from bs4 import BeautifulSoup

class SCCourtsScraper:
    def __init__(self):
        self.base_url = "https://publicindex.sccourts.org"
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        self.proxy = "{working_proxy['proxy']}"
        self.proxy_dict = {{
            'http': f'http://{{self.proxy}}',
            'https': f'http://{{self.proxy}}'
        }}
        
        self.session = requests.Session()
        self.session.proxies.update(self.proxy_dict)
        
        self.headers = {{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }}
        
        self.session.headers.update(self.headers)
    
    def make_request(self):
        """
        Make request to the target URL
        """
        try:
            print(f"🌐 Making request through proxy: {{self.proxy}}")
            response = self.session.get(self.target_url, timeout=30)
            
            print(f"📊 Status Code: {{response.status_code}}")
            
            if response.status_code == 200:
                if 'Incapsula' in response.text:
                    print("⚠️ Incapsula protection detected")
                    return False
                else:
                    print("✅ SUCCESS! No protection detected")
                    return response
            else:
                print(f"❌ Error: {{response.status_code}}")
                return False
                
        except Exception as e:
            print(f"❌ Request failed: {{e}}")
            return False
    
    def parse_content(self, response):
        """
        Parse the HTML content
        """
        if not response:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for forms
        forms = soup.find_all('form')
        print(f"📝 Found {{len(forms)}} forms")
        
        # Look for input fields
        inputs = soup.find_all('input')
        print(f"🔍 Found {{len(inputs)}} input fields")
        
        # Look for select elements
        selects = soup.find_all('select')
        print(f"📋 Found {{len(selects)}} select elements")
        
        # Look for links
        links = soup.find_all('a')
        print(f"🔗 Found {{len(links)}} links")
        
        # Look for scripts
        scripts = soup.find_all('script')
        print(f"📜 Found {{len(scripts)}} scripts")
        
        return {{
            'forms': forms,
            'inputs': inputs,
            'selects': selects,
            'links': links,
            'scripts': scripts
        }}
    
    def run(self):
        """
        Run the scraper
        """
        print("🚀 Starting SC Courts Scraper with Proxy")
        print("=" * 50)
        
        # Make request
        response = self.make_request()
        
        if response:
            # Parse content
            parsed_data = self.parse_content(response)
            
            if parsed_data:
                print("✅ Scraping successful!")
                return parsed_data
            else:
                print("❌ Failed to parse content")
                return None
        else:
            print("❌ Request failed")
            return None

def main():
    scraper = SCCourtsScraper()
    result = scraper.run()
    
    if result:
        print("🎉 Scraping completed successfully!")
    else:
        print("❌ Scraping failed")

if __name__ == "__main__":
    main()
'''
            
            with open('sc_courts_scraper_proxy.py', 'w') as f:
                f.write(scraper_code)
            
            print("💾 Created sc_courts_scraper_proxy.py")
            print("🚀 Run: python sc_courts_scraper_proxy.py")

def main():
    # The proxy list you provided
    proxy_text = """104.233.26.241	6079	US	United States	transparent	no	no	31 mins ago
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
    
    print("🧪 TESTING PROXY LIST FOR SC COURTS ACCESS")
    print("=" * 60)
    
    tester = ProxyTester()
    
    # Parse the proxy list
    proxies = tester.parse_proxy_list(proxy_text)
    
    if not proxies:
        print("❌ No US proxies found in the list")
        return
    
    # Test all proxies
    results = tester.test_all_proxies(max_workers=3)
    
    # Show summary
    print("\n📊 TESTING SUMMARY")
    print("=" * 40)
    
    success_count = len([r for r in results if r['status'] == 'success'])
    incapsula_count = len([r for r in results if r['status'] == 'incapsula'])
    blocked_count = len([r for r in results if r['status'] == 'blocked'])
    error_count = len([r for r in results if r['status'] == 'error'])
    
    print(f"✅ Success: {success_count}")
    print(f"⚠️ Incapsula: {incapsula_count}")
    print(f"❌ Blocked: {blocked_count}")
    print(f"💥 Errors: {error_count}")
    
    if success_count > 0:
        print(f"\n🎉 FOUND {success_count} WORKING PROXIES!")
        tester.save_working_proxies()
        tester.create_scraper_with_proxy()
    else:
        print("\n❌ No working proxies found")
        print("💡 Try different proxy sources or use VPN")

if __name__ == "__main__":
    main()
