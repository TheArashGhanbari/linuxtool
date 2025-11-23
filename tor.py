#!/usr/bin/env python3
import requests
import socks
import socket
import time
import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


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
        socket.socket = socket.socket
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
    """Check Tor service status - REAL check"""
    print(f"{Fore.CYAN}Checking Tor service status...{Style.RESET_ALL}")

    try:
        # Method 1: Check systemctl
        result = subprocess.run(["systemctl", "is-active", "tor"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip() == "active":
            return True

        # Method 2: Check if Tor process is running
        result = subprocess.run(["pgrep", "-x", "tor"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            return True

        # Method 3: Check if Tor port is listening
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
        if ":9050" in result.stdout or ":9051" in result.stdout:
            return True

        return False
    except:
        return False


def start_tor_service():
    """Try to start Tor service"""
    print(f"{Fore.YELLOW}Attempting to start Tor service...{Style.RESET_ALL}")
    try:
        result = subprocess.run(["sudo", "systemctl", "start", "tor"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ Tor service started successfully{Style.RESET_ALL}")
            # Wait a bit for Tor to initialize
            time.sleep(3)
            return True
        else:
            print(f"{Fore.RED}❌ Failed to start Tor service{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Error: {result.stderr}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error starting Tor: {e}{Style.RESET_ALL}")
        return False


def show_tor_menu():
    """Show Tor tool menu"""
    menu = f"""
{Fore.CYAN}=== Tor Connection Tool ==={Style.RESET_ALL}

{Fore.YELLOW}1.{Style.RESET_ALL} Check Tor Connection Status
{Fore.YELLOW}2.{Style.RESET_ALL} Test Tor Requests
{Fore.YELLOW}3.{Style.RESET_ALL} Start Tor Service
{Fore.YELLOW}4.{Style.RESET_ALL} Show Usage Examples
{Fore.YELLOW}5.{Style.RESET_ALL} Return to Main Menu

{Fore.CYAN}Select an option (1-5): {Style.RESET_ALL}"""
    print(menu)


def show_usage_examples():
    """Show usage examples for Tor"""
    clear_screen()
    print(f"{Fore.CYAN}=== Tor Usage Examples ==={Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Basic Usage with requests:{Style.RESET_ALL}")
    print("""
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

response = requests.get('http://example.com', proxies=proxies)
print(response.text)
    """)

    print(f"\n{Fore.GREEN}Using socks directly:{Style.RESET_ALL}")
    print("""
import socks
import socket
import requests

# Set up Tor proxy
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

# Now all requests go through Tor
response = requests.get('http://example.com')
print(response.text)

# Reset to normal connection
socks.set_default_proxy()
socket.socket = socket.socket
    """)

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def check_tor_status_detailed():
    """Detailed Tor status check with clear output"""
    clear_screen()
    print(f"{Fore.CYAN}=== Tor Status Check ==={Style.RESET_ALL}\n")

    # Check Tor service
    print(f"{Fore.CYAN}Checking Tor service status...{Style.RESET_ALL}")
    if tor_status():
        print(f"{Fore.GREEN}✅ Tor service is running{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Tor service is not running{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please start Tor service using option 3{Style.RESET_ALL}")
        return

    # Test Tor connection
    print(f"\n{Fore.CYAN}Checking Tor connection...{Style.RESET_ALL}")
    tor_ip, real_ip, is_working = check_tor_connection()

    if is_working and tor_ip and real_ip:
        print(f"{Fore.GREEN}✅ Tor connection is working!{Style.RESET_ALL}")
        print(f"📡 Real IP: {real_ip}")
        print(f"🕵️ Tor IP: {tor_ip}")
        print(f"{Fore.GREEN}✅ You are anonymous!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Tor connection failed{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Please make sure Tor is running on 127.0.0.1:9050{Style.RESET_ALL}")

    # Additional Tor test
    print(f"\n{Fore.CYAN}Testing with Tor Project...{Style.RESET_ALL}")
    success, message = test_tor_requests()
    if success:
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def main():
    while True:
        clear_screen()
        print(f"{Fore.YELLOW}=== Tor Connection Tool ==={Style.RESET_ALL}")
        show_tor_menu()

        try:
            choice = input().strip()

            if choice == '1':
                check_tor_status_detailed()
                input(
                    f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

            elif choice == '2':
                clear_screen()
                print(f"{Fore.YELLOW}=== Test Tor Requests ==={Style.RESET_ALL}\n")
                success, message = test_tor_requests()
                if success:
                    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                input(
                    f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

            elif choice == '3':
                clear_screen()
                print(f"{Fore.YELLOW}=== Start Tor Service ==={Style.RESET_ALL}\n")
                if start_tor_service():
                    # Verify it started
                    time.sleep(2)
                    if tor_status():
                        print(
                            f"{Fore.GREEN}✅ Tor service is now running!{Style.RESET_ALL}")
                    else:
                        print(
                            f"{Fore.RED}❌ Tor service may not have started properly{Style.RESET_ALL}")
                input(
                    f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

            elif choice == '4':
                show_usage_examples()

            elif choice == '5':
                print(f"{Fore.GREEN}Returning to main menu...{Style.RESET_ALL}")
                time.sleep(1)
                break
            else:
                print(
                    f"{Fore.RED}Invalid choice! Please select 1-5{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
            time.sleep(1)
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
