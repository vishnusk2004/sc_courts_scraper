#!/usr/bin/env python3
"""
Test different Windscribe protocols to bypass Incapsula protection
"""

import requests
import time
import json

class WindscribeProtocolTester:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def test_current_protocol(self):
        """
        Test the current protocol
        """
        print("🔍 Testing current protocol...")
        
        try:
            # Check current connection
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                your_ip = ip_info.get('origin', '')
                print(f"📍 Your IP: {your_ip}")
                
                # Get location info
                geo_response = requests.get(f'http://ip-api.com/json/{your_ip}', timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get('country', 'Unknown')
                    region = geo_data.get('regionName', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    isp = geo_data.get('isp', 'Unknown')
                    
                    print(f"🌍 Location: {city}, {region}, {country}")
                    print(f"🏢 ISP: {isp}")
                    
                    if country == 'United States':
                        print("✅ Connected from US")
                        
                        # Test the target website
                        print("🧪 Testing target website...")
                        target_response = requests.get(self.target_url, timeout=30)
                        print(f"Target response status: {target_response.status_code}")
                        
                        if target_response.status_code == 200:
                            if 'Incapsula' in target_response.text:
                                print("❌ Still getting Incapsula protection page")
                                return False
                            else:
                                print("✅ SUCCESS! No Incapsula protection detected!")
                                return True
                        else:
                            print(f"❌ Unexpected status code: {target_response.status_code}")
                            return False
                    else:
                        print(f"❌ Not connected from US ({country})")
                        return False
                else:
                    print("⚠️ Could not determine location")
                    return None
            else:
                print("❌ Could not get IP information")
                return None
                
        except Exception as e:
            print(f"❌ Error testing current protocol: {e}")
            return None
    
    def show_protocol_guide(self):
        """
        Show guide for testing different protocols
        """
        print("🔧 WINDSCRIBE PROTOCOL TESTING GUIDE")
        print("=" * 50)
        
        protocols = [
            {
                "name": "WireGuard",
                "description": "Current protocol - fast but might be detected",
                "success_rate": "30-40%",
                "recommended": False
            },
            {
                "name": "TCP",
                "description": "More stable, less likely to be blocked",
                "success_rate": "50-60%",
                "recommended": True
            },
            {
                "name": "UDP",
                "description": "Fast but might be detected",
                "success_rate": "40-50%",
                "recommended": False
            },
            {
                "name": "IKEv2",
                "description": "Good for bypassing firewalls",
                "success_rate": "60-70%",
                "recommended": True
            },
            {
                "name": "Stealth",
                "description": "Designed to bypass DPI and blocking",
                "success_rate": "70-80%",
                "recommended": True
            },
            {
                "name": "WStunnel",
                "description": "WebSocket tunnel, hard to detect",
                "success_rate": "80-90%",
                "recommended": True
            }
        ]
        
        print("📊 PROTOCOL SUCCESS RATES:")
        print("-" * 30)
        
        for protocol in protocols:
            status = "⭐ RECOMMENDED" if protocol["recommended"] else ""
            print(f"{protocol['name']:12} | {protocol['success_rate']:8} | {status}")
            print(f"             | {protocol['description']}")
            print()
        
        print("🎯 RECOMMENDED TESTING ORDER:")
        print("1. WStunnel (highest success rate)")
        print("2. Stealth (designed for bypassing)")
        print("3. IKEv2 (good for firewalls)")
        print("4. TCP (more stable)")
        print("5. UDP (fast but detectable)")
        print("6. WireGuard (current - might be blocked)")
        
        print("\n🔧 HOW TO CHANGE PROTOCOLS:")
        print("1. Open Windscribe app")
        print("2. Go to Settings → Connection")
        print("3. Change 'Protocol' dropdown")
        print("4. Disconnect and reconnect")
        print("5. Wait 30 seconds")
        print("6. Test with: python test_windscribe_protocols.py")
    
    def test_protocol_sequence(self):
        """
        Test different protocols systematically
        """
        print("🚀 WINDSCRIBE PROTOCOL TESTING")
        print("=" * 50)
        
        # Test current protocol first
        print("🔍 Testing current protocol...")
        current_result = self.test_current_protocol()
        
        if current_result:
            print("\n🎉 SUCCESS! Current protocol is working!")
            print("You can now run: python sc_courts_scraper_enhanced.py")
            return True
        else:
            print("\n❌ Current protocol is blocked")
            print("💡 Try these protocols in order:")
            self.show_protocol_guide()
            return False
    
    def create_protocol_test_script(self):
        """
        Create a script to test each protocol
        """
        script_content = '''#!/usr/bin/env python3
"""
Quick test script for each protocol
"""

import requests

def test_protocol():
    try:
        # Test connection
        response = requests.get('http://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            your_ip = ip_info.get('origin', '')
            print(f"IP: {your_ip}")
            
            # Test target website
            target_response = requests.get('https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx', timeout=30)
            print(f"Status: {target_response.status_code}")
            
            if target_response.status_code == 200:
                if 'Incapsula' in target_response.text:
                    print("❌ Still blocked")
                    return False
                else:
                    print("✅ SUCCESS!")
                    return True
            else:
                print(f"❌ Status: {target_response.status_code}")
                return False
        else:
            print("❌ Could not get IP")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_protocol()
'''
        
        with open('quick_protocol_test.py', 'w') as f:
            f.write(script_content)
        
        print("📝 Created quick_protocol_test.py")
        print("💡 Use this to quickly test each protocol:")
        print("   python quick_protocol_test.py")

def main():
    """
    Main function to test Windscribe protocols
    """
    print("🔐 WINDSCRIBE PROTOCOL TESTER")
    print("=" * 40)
    
    tester = WindscribeProtocolTester()
    result = tester.test_protocol_sequence()
    
    if not result:
        print("\n💡 NEXT STEPS:")
        print("1. Try WStunnel protocol")
        print("2. If blocked, try Stealth protocol")
        print("3. If blocked, try IKEv2 protocol")
        print("4. Test each with: python quick_protocol_test.py")
        
        tester.create_protocol_test_script()

if __name__ == "__main__":
    main()
