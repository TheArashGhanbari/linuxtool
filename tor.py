#!/usr/bin/env python3
import requests
import socks
import socket
import time
from colorama import Fore, Style, init

init(autoreset=True)


def check_tor_connection():
    """Check if Tor connection is working"""
    print(f"{Fore.CYAN}Checking Tor connection...{Style.RESET_ALL}")

    # Set up Tor proxy
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    try:
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        tor_ip = response.text.strip()

        # Reset to direct connection for comparison
        socks.set_default_proxy()
        socket.socket = socket._socketobject
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        real_ip = response.text.strip()

        return tor_ip, real_ip, tor_ip != real_ip
    except Exception as e:
        return None, None, False


def test_tor_requests():
    """Test making requests through Tor"""
    print(f"{Fore.CYAN}Testing Tor requests...{Style.RESET_ALL}")

    session = requests.Session()
    session.proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    try:
        # Test with a known Tor-friendly site
        response = session.get("https://check.torproject.org", timeout=10)
        if "Congratulations" in response.text:
            return True, "✅ Connected to Tor successfully!"
        else:
            return False, "❌ Not connected through Tor"
    except Exception as e:
        return False, f"❌ Connection failed: {e}"


def tor_status():
    """Check Tor service status"""
    print(f"{Fore.CYAN}Checking Tor service status...{Style.RESET_ALL}")

    try:
        import subprocess
        result = subprocess.run(["systemctl", "is-active", "tor"],
                                capture_output=True, text=True)
        return result.stdout.strip() == "active"
    except:
        return False


def main():
    print(f"{Fore.YELLOW}=== Tor Connection Tool ==={Style.RESET_ALL}\n")

    # Check Tor service
    if tor_status():
        print(f"{Fore.GREEN}✅ Tor service is running{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Tor service is not running{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please start Tor service:{Style.RESET_ALL}")
        print("sudo systemctl start tor")
        return

    # Test Tor connection
    tor_ip, real_ip, is_working = check_tor_connection()

    if is_working:
        print(f"{Fore.GREEN}✅ Tor connection is working!{Style.RESET_ALL}")
        print(f"Real IP: {real_ip}")
        print(f"Tor IP: {tor_ip}")
    else:
        print(f"{Fore.RED}❌ Tor connection failed{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Please make sure Tor is running on 127.0.0.1:9050{Style.RESET_ALL}")

    # Additional Tor test
    print("\n" + "="*40)
    success, message = test_tor_requests()
    if success:
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")

    # Show usage example
    print(f"\n{Fore.CYAN}Usage Example:{Style.RESET_ALL}")
    print("""
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

response = requests.get('http://example.com', proxies=proxies)
print(response.text)
    """)

    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
