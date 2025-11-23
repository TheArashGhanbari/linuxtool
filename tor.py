#!/usr/bin/env python3
import requests
import socks
import socket
import subprocess
import sys
from typing import Optional, Dict, Any


class TorManager:
    def __init__(self):
        self.tor_proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        self.is_connected = False

    def check_tor_connection(self) -> bool:
        """Check if Tor connection is working"""
        try:
            session = requests.Session()
            session.proxies = self.tor_proxy
            response = session.get('http://httpbin.org/ip', timeout=10)

            if response.status_code == 200:
                tor_ip = response.json().get('origin', '')
                print(f"✅ Tor Connected - Your IP: {tor_ip}")
                return True
            return False
        except:
            return False

    def get_tor_info(self) -> Dict[str, Any]:
        """Get detailed Tor information"""
        try:
            session = requests.Session()
            session.proxies = self.tor_proxy

            # Get IP information
            ip_response = session.get('http://httpbin.org/ip', timeout=10)
            user_agent_response = session.get(
                'http://httpbin.org/user-agent', timeout=10)

            info = {
                'tor_ip': ip_response.json().get('origin', 'Unknown') if ip_response.status_code == 200 else 'Unknown',
                'user_agent': user_agent_response.json().get('user-agent', 'Unknown') if user_agent_response.status_code == 200 else 'Unknown',
                'status': 'Connected' if self.check_tor_connection() else 'Disconnected'
            }

            return info
        except Exception as e:
            return {
                'tor_ip': 'Unknown',
                'user_agent': 'Unknown',
                'status': f'Error: {str(e)}'
            }

    def setup_tor_proxy(self):
        """Setup system to use Tor proxy"""
        try:
            # Set up socket to use Tor
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            # Test the connection
            if self.check_tor_connection():
                self.is_connected = True
                print("🔒 All traffic is now routed through Tor")
                return True
            else:
                print("❌ Failed to route traffic through Tor")
                return False

        except Exception as e:
            print(f"❌ Error setting up Tor proxy: {e}")
            return False

    def restore_normal_connection(self):
        """Restore normal connection (disable Tor)"""
        try:
            # Reset socket to default
            socks.set_default_proxy()

            # Test normal connection
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                real_ip = response.json().get('origin', '')
                print(f"🌐 Normal connection restored - Your IP: {real_ip}")
                self.is_connected = False
                return True
            return False
        except Exception as e:
            print(f"❌ Error restoring normal connection: {e}")
            return False


def test_tor_connection():
    """Test function to check Tor connectivity"""
    tor_mgr = TorManager()

    print("🔍 Testing Tor connection...")
    if tor_mgr.check_tor_connection():
        info = tor_mgr.get_tor_info()
        print("\n📊 Tor Connection Info:")
        print(f"   IP Address: {info['tor_ip']}")
        print(f"   User Agent: {info['user_agent']}")
        print(f"   Status: {info['status']}")
    else:
        print("❌ Tor is not connected or not running")
        print("💡 Make sure Tor service is running on port 9050")


if __name__ == "__main__":
    test_tor_connection()
