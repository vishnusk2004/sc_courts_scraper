#!/usr/bin/env python3
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
