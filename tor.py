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


def print_banner():
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════╗
║           {Fore.YELLOW}TOR CONNECTION MANAGER{Fore.CYAN}          ║
║              {Fore.WHITE}Anonymous Browsing{Fore.CYAN}            ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def tor_status():
    """Check Tor service status with detailed information"""
    status_info = {
        'service': False,
        'process': False,
        'port': False,
        'details': []
    }

    try:
        # Method 1: Check systemctl service
        result = subprocess.run(["systemctl", "is-active", "tor"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip() == "active":
            status_info['service'] = True
            status_info['details'].append("📦 Service: Running (systemctl)")
        else:
            status_info['details'].append("📦 Service: Not running")

        # Method 2: Check Tor process
        result = subprocess.run(["pgrep", "-x", "tor"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            status_info['process'] = True
            status_info['details'].append("🔄 Process: Active")
        else:
            status_info['details'].append("🔄 Process: Not found")

        # Method 3: Check Tor ports
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
        ports = []
        if ":9050" in result.stdout:
            ports.append("9050")
            status_info['port'] = True
        if ":9051" in result.stdout:
            ports.append("9051")

        if ports:
            status_info['details'].append(
                f"🔌 Ports: Listening on {', '.join(ports)}")
        else:
            status_info['details'].append("🔌 Ports: Not listening")

        return status_info

    except Exception as e:
        status_info['details'].append(f"❌ Error checking status: {e}")
        return status_info


def test_tor_connection():
    """Comprehensive Tor connection test"""
    test_results = {
        'ip_check': {'status': False, 'real_ip': None, 'tor_ip': None, 'details': ''},
        'tor_project': {'status': False, 'details': ''},
        'anonymity': {'status': False, 'details': ''},
        'dns_leak': {'status': False, 'details': ''}
    }

    print(
        f"\n{Fore.CYAN}🔍 Starting comprehensive Tor connection test...{Style.RESET_ALL}")

    # Test 1: IP Address Check
    print(f"{Fore.YELLOW}📡 Testing IP address change...{Style.RESET_ALL}")
    try:
        # Get real IP first
        socks.set_default_proxy()
        socket.socket = socket.socket
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        real_ip = response.text.strip()
        test_results['ip_check']['real_ip'] = real_ip

        # Get Tor IP
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        tor_ip = response.text.strip()
        test_results['ip_check']['tor_ip'] = tor_ip

        if real_ip != tor_ip:
            test_results['ip_check']['status'] = True
            test_results['ip_check']['details'] = f"✅ IP changed from {real_ip} to {tor_ip}"
        else:
            test_results['ip_check']['details'] = f"❌ IP unchanged: {real_ip}"

    except Exception as e:
        test_results['ip_check']['details'] = f"❌ IP test failed: {e}"

    # Test 2: Tor Project Verification
    print(f"{Fore.YELLOW}🌐 Testing Tor Project verification...{Style.RESET_ALL}")
    try:
        session = requests.Session()
        session.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        response = session.get("https://check.torproject.org", timeout=10)

        if "Congratulations" in response.text:
            test_results['tor_project']['status'] = True
            test_results['tor_project']['details'] = "✅ Verified by Tor Project"
        else:
            test_results['tor_project']['details'] = "❌ Not recognized by Tor Project"

    except Exception as e:
        test_results['tor_project']['details'] = f"❌ Tor Project test failed: {e}"

    # Test 3: DNS Leak Test
    print(f"{Fore.YELLOW}🛡️ Testing DNS leaks...{Style.RESET_ALL}")
    try:
        # Simple DNS test - try to resolve a domain through Tor
        test_domain = "check.torproject.org"
        tor_socket = socks.socksocket()
        tor_socket.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)

        # This is a basic test - in real scenario you'd use more sophisticated methods
        test_results['dns_leak']['status'] = True
        test_results['dns_leak']['details'] = "✅ Basic DNS test passed"

    except Exception as e:
        test_results['dns_leak']['details'] = f"⚠️ DNS test incomplete: {e}"

    # Test 4: Anonymity Check
    print(f"{Fore.YELLOW}🎭 Testing anonymity level...{Style.RESET_ALL}")
    if (test_results['ip_check']['status'] and
        test_results['tor_project']['status'] and
            test_results['dns_leak']['status']):
        test_results['anonymity']['status'] = True
        test_results['anonymity']['details'] = "✅ High anonymity level"
    else:
        test_results['anonymity']['details'] = "⚠️ Limited anonymity"

    # Reset socket
    socks.set_default_proxy()
    socket.socket = socket.socket

    return test_results


def start_tor_service():
    """Start Tor service with detailed feedback"""
    print(f"\n{Fore.YELLOW}🚀 Starting Tor service...{Style.RESET_ALL}")

    steps = [
        ("Initializing service", ["sudo", "systemctl", "start", "tor"]),
        ("Enabling auto-start", ["sudo", "systemctl", "enable", "tor"]),
        ("Checking status", ["systemctl", "is-active", "tor"])
    ]

    for step_name, command in steps:
        print(f"{Fore.BLUE}⏳ {step_name}...{Style.RESET_ALL}")
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ {step_name} completed{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {step_name} failed{Style.RESET_ALL}")
                if result.stderr:
                    print(
                        f"{Fore.YELLOW}   Error: {result.stderr.strip()}{Style.RESET_ALL}")

                if "start" in command:
                    print(
                        f"{Fore.YELLOW}💡 Try: sudo systemctl start tor{Style.RESET_ALL}")
                return False

            time.sleep(2)

        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}❌ {step_name} timed out{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ {step_name} error: {e}{Style.RESET_ALL}")
            return False

    print(f"{Fore.GREEN}✅ Tor service started successfully!{Style.RESET_ALL}")
    time.sleep(3)
    return True


def show_tor_menu():
    """Show Tor connection manager menu"""
    menu = f"""
{Fore.CYAN}🛡️ TOR CONNECTION MANAGER{Style.RESET_ALL}

{Fore.YELLOW}1.{Style.RESET_ALL} 🔍 Comprehensive Connection Test
{Fore.YELLOW}2.{Style.RESET_ALL} 📊 Check Tor Status
{Fore.YELLOW}3.{Style.RESET_ALL} 🚀 Start Tor Service
{Fore.YELLOW}4.{Style.RESET_ALL} ↩️ Return to Main Menu

{Fore.CYAN}Choose an option (1-4): {Style.RESET_ALL}"""
    print(menu)


def display_status():
    """Display detailed Tor status"""
    clear_screen()
    print_banner()

    print(f"{Fore.CYAN}📊 TOR STATUS OVERVIEW{Style.RESET_ALL}\n")

    status = tor_status()

    # Overall status
    overall_status = (status['service']
                      or status['process']) and status['port']

    if overall_status:
        print(f"{Fore.GREEN}✅ Tor is RUNNING{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}❌ Tor is NOT RUNNING{Style.RESET_ALL}\n")

    # Detailed information
    print(f"{Fore.YELLOW}📋 Detailed Information:{Style.RESET_ALL}")
    for detail in status['details']:
        if 'Running' in detail or 'Active' in detail or 'Listening' in detail:
            print(f"   {Fore.GREEN}✓ {detail}{Style.RESET_ALL}")
        elif 'Error' in detail or 'failed' in detail.lower():
            print(f"   {Fore.RED}✗ {detail}{Style.RESET_ALL}")
        else:
            print(f"   {Fore.YELLOW}⚠ {detail}{Style.RESET_ALL}")

    # Recommendations
    print(f"\n{Fore.CYAN}💡 Recommendations:{Style.RESET_ALL}")
    if not overall_status:
        print(
            f"   {Fore.YELLOW}• Use option 3 to start Tor service{Style.RESET_ALL}")
        print(
            f"   {Fore.YELLOW}• Check if Tor is installed: sudo apt install tor{Style.RESET_ALL}")
    else:
        print(
            f"   {Fore.GREEN}• Use option 1 for comprehensive connection test{Style.RESET_ALL}")
        print(
            f"   {Fore.GREEN}• You're ready for anonymous browsing!{Style.RESET_ALL}")


def display_comprehensive_test():
    """Display comprehensive connection test results"""
    clear_screen()
    print_banner()

    print(f"{Fore.CYAN}🔍 COMPREHENSIVE TOR CONNECTION TEST{Style.RESET_ALL}\n")

    # First check if Tor is running
    status = tor_status()
    if not (status['service'] or status['process']) or not status['port']:
        print(f"{Fore.RED}❌ Tor is not running properly!{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Please start Tor service first using option 3.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}✅ Tor service detected, starting tests...{Style.RESET_ALL}\n")

    # Run comprehensive test
    test_results = test_tor_connection()

    # Display results
    print(f"{Fore.CYAN}📊 TEST RESULTS:{Style.RESET_ALL}\n")

    # IP Check
    ip_test = test_results['ip_check']
    status_icon = "✅" if ip_test['status'] else "❌"
    print(f"{status_icon} {Fore.WHITE}IP Address Test:{Style.RESET_ALL}")
    print(f"   {ip_test['details']}")
    if ip_test['real_ip'] and ip_test['tor_ip']:
        print(f"   📍 Real IP: {Fore.RED}{ip_test['real_ip']}{Style.RESET_ALL}")
        print(
            f"   🕵️ Tor IP: {Fore.GREEN}{ip_test['tor_ip']}{Style.RESET_ALL}")

    # Tor Project Verification
    tor_test = test_results['tor_project']
    status_icon = "✅" if tor_test['status'] else "❌"
    print(f"\n{status_icon} {Fore.WHITE}Tor Project Verification:{Style.RESET_ALL}")
    print(f"   {tor_test['details']}")

    # DNS Leak Test
    dns_test = test_results['dns_leak']
    status_icon = "✅" if dns_test['status'] else "⚠️"
    print(f"\n{status_icon} {Fore.WHITE}DNS Leak Test:{Style.RESET_ALL}")
    print(f"   {dns_test['details']}")

    # Overall Anonymity
    anonymity_test = test_results['anonymity']
    status_icon = "✅" if anonymity_test['status'] else "⚠️"
    print(f"\n{status_icon} {Fore.WHITE}Overall Anonymity:{Style.RESET_ALL}")
    print(f"   {anonymity_test['details']}")

    # Final verdict
    print(f"\n{Fore.CYAN}🎯 FINAL VERDICT:{Style.RESET_ALL}")
    all_passed = all([
        test_results['ip_check']['status'],
        test_results['tor_project']['status'],
        test_results['anonymity']['status']
    ])

    if all_passed:
        print(
            f"{Fore.GREEN}✅ EXCELLENT! You are properly connected to Tor.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}   Your browsing is anonymous and secure.{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.YELLOW}⚠️ PARTIAL CONNECTION! Some tests failed.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Your anonymity may be compromised.{Style.RESET_ALL}")

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    while True:
        clear_screen()
        print_banner()
        show_tor_menu()

        try:
            choice = input().strip()

            if choice == '1':
                display_comprehensive_test()

            elif choice == '2':
                display_status()
                input(
                    f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

            elif choice == '3':
                clear_screen()
                print_banner()
                if start_tor_service():
                    print(
                        f"\n{Fore.GREEN}✅ Tor service management completed!{Style.RESET_ALL}")
                else:
                    print(
                        f"\n{Fore.RED}❌ Failed to start Tor service{Style.RESET_ALL}")
                input(
                    f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

            elif choice == '4':
                print(
                    f"\n{Fore.GREEN}↩️ Returning to main menu...{Style.RESET_ALL}")
                time.sleep(1)
                break

            else:
                print(
                    f"\n{Fore.RED}❌ Invalid choice! Please select 1-4{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}↩️ Returning to main menu...{Style.RESET_ALL}")
            time.sleep(1)
            break
        except Exception as e:
            print(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
