#!/usr/bin/env python3
"""
Comprehensive troubleshooting guide for SC Courts scraper
"""

import requests
import time

class TroubleshootingGuide:
    def __init__(self):
        self.target_url = "https://publicindex.sccourts.org/dorchester/courtrosters/RosterSelection.aspx"
        
    def check_current_status(self):
        """
        Check current connection and website access
        """
        print("🔍 COMPREHENSIVE STATUS CHECK")
        print("=" * 50)
        
        # Check IP and location
        try:
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
                        print("\n🧪 Testing target website...")
                        try:
                            target_response = requests.get(self.target_url, timeout=30)
                            print(f"Target response status: {target_response.status_code}")
                            
                            if target_response.status_code == 200:
                                if 'Incapsula' in target_response.text:
                                    print("⚠️ Getting Incapsula protection page")
                                    return "incapsula"
                                else:
                                    print("✅ SUCCESS! No protection detected!")
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
    
    def provide_solutions(self, status):
        """
        Provide solutions based on current status
        """
        print("\n💡 SOLUTIONS BASED ON CURRENT STATUS")
        print("=" * 50)
        
        if status == "success":
            print("🎉 SUCCESS! You can now scrape the website!")
            print("Run: python sc_courts_scraper_enhanced.py")
            
        elif status == "incapsula":
            print("⚠️ INCAPSULA PROTECTION DETECTED")
            print("Solutions:")
            print("1. Try different US VPN server")
            print("2. Try different time of day")
            print("3. Try different VPN provider")
            print("4. Try browser extensions")
            
        elif status == "blocked":
            print("❌ IP BLOCKED (403 Forbidden)")
            print("Solutions:")
            print("1. Switch to different US VPN server")
            print("2. Try different Windscribe protocol")
            print("3. Try different VPN provider")
            print("4. Wait and try again later")
            
        elif status == "not_us":
            print("❌ NOT CONNECTED FROM US")
            print("Solutions:")
            print("1. Connect to US VPN server")
            print("2. Check VPN connection")
            print("3. Try different US server")
            
        elif status == "error":
            print("❌ CONNECTION ERROR")
            print("Solutions:")
            print("1. Check internet connection")
            print("2. Restart VPN")
            print("3. Try different server")
            
        else:
            print("⚠️ UNKNOWN STATUS")
            print("Solutions:")
            print("1. Try different US VPN server")
            print("2. Try different time")
            print("3. Try different VPN provider")
    
    def show_windscribe_troubleshooting(self):
        """
        Show Windscribe-specific troubleshooting
        """
        print("\n🔧 WINDSCRIBE TROUBLESHOOTING")
        print("=" * 40)
        
        print("1. 📍 Try different US servers:")
        print("   - US East - Washington DC (recommended)")
        print("   - US East - Atlanta")
        print("   - US West - Los Angeles")
        print("   - US Central - Chicago")
        
        print("\n2. 🔧 Try different protocols:")
        print("   - WStunnel (if not already using)")
        print("   - Stealth (if available)")
        print("   - IKEv2")
        print("   - TCP")
        
        print("\n3. ⏰ Try different times:")
        print("   - Early morning (6-8 AM EST)")
        print("   - Late evening (10 PM - 12 AM EST)")
        print("   - Weekends")
        
        print("\n4. 🔄 Restart sequence:")
        print("   - Disconnect from Windscribe")
        print("   - Wait 30 seconds")
        print("   - Connect to different US server")
        print("   - Wait 30 seconds")
        print("   - Test again")
    
    def show_alternative_solutions(self):
        """
        Show alternative solutions
        """
        print("\n🚀 ALTERNATIVE SOLUTIONS")
        print("=" * 40)
        
        print("1. 🆓 FREE VPN ALTERNATIVES:")
        print("   - ProtonVPN Free")
        print("   - TunnelBear Free")
        print("   - Windscribe (different server)")
        
        print("\n2. 🌐 BROWSER EXTENSIONS:")
        print("   - Hola VPN (Chrome/Firefox)")
        print("   - Touch VPN (Chrome)")
        
        print("\n3. ☁️ FREE CLOUD SERVERS:")
        print("   - Oracle Cloud Always Free")
        print("   - Google Cloud Free Tier")
        
        print("\n4. 💰 PAID SOLUTIONS:")
        print("   - Residential proxy services")
        print("   - Premium VPN services")
    
    def create_test_script(self):
        """
        Create a simple test script
        """
        script_content = '''#!/usr/bin/env python3
"""
Quick test script for SC Courts scraper
"""

import requests

def test_sc_courts():
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
                    print("Incapsula protection detected")
                    return False
                else:
                    print("SUCCESS! No protection detected")
                    return True
            else:
                print(f"Blocked with status: {target_response.status_code}")
                return False
        else:
            print("Could not get IP")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_sc_courts()
'''
        
        with open('test_sc_courts.py', 'w') as f:
            f.write(script_content)
        
        print("\n📝 Created test_sc_courts.py")
        print("💡 Use this to quickly test your connection:")
        print("   python test_sc_courts.py")

def main():
    """
    Main troubleshooting function
    """
    print("🔧 SC COURTS SCRAPER TROUBLESHOOTING")
    print("=" * 60)
    
    guide = TroubleshootingGuide()
    
    # Check current status
    status = guide.check_current_status()
    
    # Provide solutions
    guide.provide_solutions(status)
    
    # Show Windscribe troubleshooting
    guide.show_windscribe_troubleshooting()
    
    # Show alternative solutions
    guide.show_alternative_solutions()
    
    # Create test script
    guide.create_test_script()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Try different US VPN server")
    print("2. Test with: python test_sc_courts.py")
    print("3. If working, run: python sc_courts_scraper_enhanced.py")

if __name__ == "__main__":
    main()
