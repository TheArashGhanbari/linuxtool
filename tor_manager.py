#!/usr/bin/env python3
import requests
import socket
import time
from stem import Signal
from stem.control import Controller
from colorama import init, Fore, Style

init()


class TorManager:
    def __init__(self):
        self.session = None
        self.tor_port = 9050
        self.control_port = 9051
        self.proxies = {
            'http': f'socks5://127.0.0.1:{self.tor_port}',
            'https': f'socks5://127.0.0.1:{self.tor_port}'
        }

    def check_tor_installation(self):
        """Check if Tor is installed on the system"""
        try:
            import subprocess
            result = subprocess.run(
                ['which', 'tor'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def is_tor_running(self):
        """Check if Tor service is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            return result == 0
        except:
            return False

    def start_tor_session(self):
        """Start a new Tor session"""
        try:
            self.session = requests.Session()
            self.session.proxies = self.proxies

            # Test Tor connection
            response = self.session.get(
                'http://check.torproject.org/', timeout=30)
            if 'Congratulations' in response.text:
                print(f"{Fore.GREEN}✅ Success: Connected to Tor{Style.RESET_ALL}")
                return True
            else:
                print(
                    f"{Fore.RED}❌ Error: Failed to connect to Tor{Style.RESET_ALL}")
                return False

        except Exception as e:
            print(f"{Fore.RED}❌ Error connecting to Tor: {e}{Style.RESET_ALL}")
            return False

    def renew_connection(self):
        """Change IP by creating new circuit"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                print(f"{Fore.YELLOW}🔄 Changing IP...{Style.RESET_ALL}")
                time.sleep(5)  # Wait for new circuit to be established
                return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error changing IP: {e}{Style.RESET_ALL}")
            return False

    def get_current_ip(self):
        """Get current IP address"""
        try:
            response = self.session.get('http://httpbin.org/ip', timeout=10)
            return response.json().get('origin', 'Unknown')
        except Exception as e:
            return f"Error: {e}"

    def make_request(self, url, method='GET', **kwargs):
        """Send request through Tor"""
        if not self.session:
            print(f"{Fore.RED}❌ Please start Tor session first{Style.RESET_ALL}")
            return None

        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except Exception as e:
            print(f"{Fore.RED}❌ Error sending request: {e}{Style.RESET_ALL}")
            return None


def tor_tool():
    """Tor Management Tool"""
    tor_manager = TorManager()

    while True:
        print(f"\n{Fore.CYAN}=== Tor Management Tool ==={Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Check Tor Status")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Start New Session")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Change IP")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Test Anonymity")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Send Custom Request")
        print(f"{Fore.RED}[0]{Style.RESET_ALL} Return to Main Menu")

        choice = input(f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")

        if choice == "1":
            print(f"\n{Fore.YELLOW}🔍 Checking Tor status...{Style.RESET_ALL}")

            if tor_manager.check_tor_installation():
                print(f"{Fore.GREEN}✅ Tor is installed on system{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Tor is not installed on system{Style.RESET_ALL}")
                print(
                    f"{Fore.YELLOW}💡 Installation guide: sudo apt install tor{Style.RESET_ALL}")

            if tor_manager.is_tor_running():
                print(f"{Fore.GREEN}✅ Tor service is running{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Tor service is not running{Style.RESET_ALL}")
                print(
                    f"{Fore.YELLOW}💡 Start service: sudo systemctl start tor{Style.RESET_ALL}")

        elif choice == "2":
            print(f"\n{Fore.YELLOW}🚀 Starting Tor session...{Style.RESET_ALL}")
            if tor_manager.start_tor_session():
                current_ip = tor_manager.get_current_ip()
                print(f"{Fore.GREEN}📡 Current IP: {current_ip}{Style.RESET_ALL}")

        elif choice == "3":
            if tor_manager.session:
                if tor_manager.renew_connection():
                    current_ip = tor_manager.get_current_ip()
                    print(f"{Fore.GREEN}🔄 New IP: {current_ip}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Please start Tor session first{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{Fore.YELLOW}🔒 Testing anonymity...{Style.RESET_ALL}")
            response = tor_manager.make_request('http://check.torproject.org/')
            if response and 'Congratulations' in response.text:
                print(f"{Fore.GREEN}✅ You are using Tor{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ You are NOT using Tor{Style.RESET_ALL}")

        elif choice == "5":
            if tor_manager.session:
                url = input(f"{Fore.CYAN}Enter URL: {Style.RESET_ALL}")
                method = input(
                    f"{Fore.CYAN}Method (GET/POST) [GET]: {Style.RESET_ALL}") or 'GET'

                response = tor_manager.make_request(url, method=method)
                if response:
                    print(
                        f"{Fore.GREEN}✅ Status: {response.status_code}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}📝 Show response? (y/n): {Style.RESET_ALL}")
                    if input().lower() == 'y':
                        print(
                            response.text[:500] + "..." if len(response.text) > 500 else response.text)
            else:
                print(f"{Fore.RED}❌ Please start Tor session first{Style.RESET_ALL}")

        elif choice == "0":
            break

        else:
            print(f"{Fore.RED}❌ Invalid option!{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}↵ Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    tor_tool()
