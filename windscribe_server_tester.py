#!/usr/bin/env python3
"""
Test different Windscribe servers for SC Courts access
"""

import requests
import time

class WindscribeServerTester:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def test_current_connection(self):
        """
        Test current connection
        """
        print("🔍 TESTING CURRENT CONNECTION")
        print("=" * 40)
        
        try:
            # Get current IP
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                your_ip = ip_info.get('origin', '')
                print(f"📍 Your IP: {your_ip}")
                
                # Get location
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
                        
                        # Test target website
                        print("\n🧪 Testing target website...")
                        try:
                            target_response = requests.get(self.target_url, timeout=30)
                            print(f"Target response status: {target_response.status_code}")
                            
                            if target_response.status_code == 200:
                                if 'Incapsula' in target_response.text:
                                    print("⚠️ Getting Incapsula protection page")
                                    return "incapsula"
                                else:
                                    print("🎉 SUCCESS! No protection detected!")
                                    return "success"
                            elif target_response.status_code == 403:
                                print("❌ 403 Forbidden - IP blocked")
                                return "blocked"
                            else:
                                print(f"❌ Unexpected status: {target_response.status_code}")
                                return "error"
                        except Exception as e:
                            print(f"❌ Error testing target: {e}")
                            return "error"
                    else:
                        print(f"❌ Not connected from US ({country})")
                        return "not_us"
                else:
                    print("⚠️ Could not determine location")
                    return "unknown"
            else:
                print("❌ Could not get IP information")
                return "error"
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            return "error"
    
    def show_windscribe_servers(self):
        """
        Show recommended Windscribe servers
        """
        print("\n🌐 RECOMMENDED WINDSCRIBE SERVERS")
        print("=" * 50)
        
        servers = [
            {
                'name': 'US East - Washington DC',
                'priority': '⭐⭐⭐⭐⭐',
                'reason': 'Highest success rate, government-friendly'
            },
            {
                'name': 'US East - Atlanta',
                'priority': '⭐⭐⭐⭐',
                'reason': 'Good for Southeast US'
            },
            {
                'name': 'US West - Los Angeles',
                'priority': '⭐⭐⭐⭐',
                'reason': 'West Coast, different IP range'
            },
            {
                'name': 'US Central - Chicago',
                'priority': '⭐⭐⭐',
                'reason': 'Central US, different region'
            },
            {
                'name': 'US East - New York',
                'priority': '⭐⭐',
                'reason': 'You tried this, might be blocked'
            }
        ]
        
        for i, server in enumerate(servers, 1):
            print(f"{i}. {server['name']} {server['priority']}")
            print(f"   💡 {server['reason']}")
            print()
    
    def show_protocols(self):
        """
        Show recommended protocols
        """
        print("🔧 RECOMMENDED PROTOCOLS")
        print("=" * 30)
        
        protocols = [
            {
                'name': 'WStunnel',
                'priority': '⭐⭐⭐⭐⭐',
                'reason': 'Most stealthy, bypasses most blocks'
            },
            {
                'name': 'Stealth',
                'priority': '⭐⭐⭐⭐',
                'reason': 'Designed to bypass restrictions'
            },
            {
                'name': 'IKEv2',
                'priority': '⭐⭐⭐',
                'reason': 'Good balance of speed and stealth'
            },
            {
                'name': 'TCP',
                'priority': '⭐⭐',
                'reason': 'Basic but reliable'
            },
            {
                'name': 'WireGuard',
                'priority': '⭐',
                'reason': 'You tried this, might be blocked'
            }
        ]
        
        for protocol in protocols:
            print(f"• {protocol['name']} {protocol['priority']}")
            print(f"  💡 {protocol['reason']}")
            print()
    
    def show_troubleshooting_steps(self):
        """
        Show troubleshooting steps
        """
        print("🔧 TROUBLESHOOTING STEPS")
        print("=" * 30)
        
        steps = [
            "1. Disconnect from Windscribe",
            "2. Wait 30 seconds",
            "3. Connect to US East - Washington DC",
            "4. Use WStunnel protocol",
            "5. Wait 30 seconds",
            "6. Test with: python test_sc_courts.py",
            "7. If blocked, try US East - Atlanta",
            "8. If still blocked, try different time"
        ]
        
        for step in steps:
            print(f"   {step}")
    
    def show_alternative_solutions(self):
        """
        Show alternative solutions
        """
        print("\n🚀 ALTERNATIVE SOLUTIONS")
        print("=" * 40)
        
        print("1. 🆓 FREE VPN ALTERNATIVES:")
        print("   • ProtonVPN Free (most reliable)")
        print("   • TunnelBear Free (500MB/month)")
        print("   • Hide.me Free (10GB/month)")
        
        print("\n2. 🌐 BROWSER EXTENSIONS:")
        print("   • Hola VPN (Chrome/Firefox)")
        print("   • Touch VPN (Chrome)")
        print("   • SetupVPN (Chrome)")
        
        print("\n3. ☁️ FREE CLOUD SERVERS:")
        print("   • Oracle Cloud Always Free")
        print("   • Google Cloud Free Tier")
        print("   • AWS Free Tier")
        
        print("\n4. 💰 PAID SOLUTIONS:")
        print("   • Residential proxy services")
        print("   • Premium VPN services")
        print("   • Dedicated US servers")

def main():
    print("🌐 WINDSCRIBE SERVER TESTER")
    print("=" * 50)
    
    tester = WindscribeServerTester()
    
    # Test current connection
    status = tester.test_current_connection()
    
    # Show recommendations
    tester.show_windscribe_servers()
    tester.show_protocols()
    tester.show_troubleshooting_steps()
    tester.show_alternative_solutions()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Try US East - Washington DC server")
    print("2. Use WStunnel protocol")
    print("3. Test with: python test_sc_courts.py")
    print("4. If blocked, try different server")

if __name__ == "__main__":
    main()
