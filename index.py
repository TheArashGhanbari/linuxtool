#!/usr/bin/env python3
import os
import sys
import requests
import socks
import socket
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global variable to track Tor status
TOR_ENABLED = False


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════╗
║           {Fore.YELLOW}LINUX TOOLKIT{Fore.CYAN}                   ║
║              {Fore.WHITE}Multi-Tool Platform{Fore.CYAN}           ║
║         {Fore.GREEN}🔒 Tor-Enabled Tools{Fore.CYAN}              ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def check_tor_connection():
    """Check if Tor connection is available"""
    try:
        # Set up Tor proxy
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # Test connection
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        tor_ip = response.text.strip()

        # Reset to direct connection for comparison
        socks.set_default_proxy()
        socket.socket = socket.socket
        response = requests.get("http://checkip.amazonaws.com", timeout=10)
        real_ip = response.text.strip()

        return tor_ip != real_ip, tor_ip, real_ip
    except:
        return False, None, None


def enable_tor_globally():
    """Enable Tor for all network requests"""
    global TOR_ENABLED
    try:
        print(f"{Fore.CYAN}🔒 Enabling Tor for all tools...{Style.RESET_ALL}")

        # Set up Tor proxy globally
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # Test if Tor is working
        is_working, tor_ip, real_ip = check_tor_connection()

        if is_working:
            TOR_ENABLED = True
            print(f"{Fore.GREEN}✅ Tor enabled successfully!{Style.RESET_ALL}")
            print(f"📡 Real IP: {real_ip}")
            print(f"🕵️ Tor IP: {tor_ip}")
            print(
                f"{Fore.GREEN}🛡️ All tools will now use Tor network{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Tor is not available{Style.RESET_ALL}")
            disable_tor_globally()
            return False

    except Exception as e:
        print(f"{Fore.RED}❌ Error enabling Tor: {e}{Style.RESET_ALL}")
        disable_tor_globally()
        return False


def disable_tor_globally():
    """Disable Tor and return to normal connection"""
    global TOR_ENABLED
    try:
        socks.set_default_proxy()
        socket.socket = socket.socket
        TOR_ENABLED = False
        print(f"{Fore.YELLOW}🔓 Tor disabled - Using normal connection{Style.RESET_ALL}")
    except:
        pass


def tor_status_menu():
    """Show Tor status and management menu"""
    while True:
        clear_screen()
        print_banner()

        print(f"{Fore.CYAN}🔒 TOR NETWORK MANAGER{Style.RESET_ALL}\n")

        # Check current status
        is_working, tor_ip, real_ip = check_tor_connection()

        if is_working:
            print(f"{Fore.GREEN}✅ Tor is ACTIVE{Style.RESET_ALL}")
            print(f"📡 Real IP: {real_ip}")
            print(f"🕵️ Tor IP: {tor_ip}")
            print(f"{Fore.GREEN}🛡️ All tools are using Tor network{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Tor is INACTIVE{Style.RESET_ALL}")
            print(
                f"{Fore.YELLOW}⚠️ Tools will use normal connection (not anonymous){Style.RESET_ALL}")

        menu = f"""
{Fore.YELLOW}1.{Style.RESET_ALL} {'🔓 Disable' if is_working else '🔒 Enable'} Tor Globally
{Fore.YELLOW}2.{Style.RESET_ALL} 📊 Check Connection Details
{Fore.YELLOW}3.{Style.RESET_ALL} ↩️ Return to Main Menu

{Fore.CYAN}Select an option (1-3): {Style.RESET_ALL}"""
        print(menu)

        choice = input().strip()

        if choice == '1':
            if is_working:
                disable_tor_globally()
                print(f"{Fore.YELLOW}Tor disabled for all tools{Style.RESET_ALL}")
            else:
                if enable_tor_globally():
                    print(f"{Fore.GREEN}Tor enabled for all tools{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to enable Tor{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == '2':
            clear_screen()
            print(f"{Fore.CYAN}🔍 Tor Connection Details{Style.RESET_ALL}\n")
            is_working, tor_ip, real_ip = check_tor_connection()

            if is_working:
                print(f"{Fore.GREEN}✅ Connection Status: ACTIVE{Style.RESET_ALL}")
                print(f"📍 Real IP: {Fore.RED}{real_ip}{Style.RESET_ALL}")
                print(f"🎭 Tor IP: {Fore.GREEN}{tor_ip}{Style.RESET_ALL}")
                print(f"🔧 Proxy: socks5://127.0.0.1:9050")
                print(f"🛡️ Anonymity: {Fore.GREEN}ENABLED{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Connection Status: INACTIVE{Style.RESET_ALL}")
                print(f"📍 Your IP: {real_ip}")
                print(f"🔧 Proxy: Direct connection")
                print(f"🛡️ Anonymity: {Fore.RED}DISABLED{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == '3':
            break

        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def show_menu():
    """Show main menu with Tor status"""
    global TOR_ENABLED

    # Check Tor status
    is_working, tor_ip, real_ip = check_tor_connection()
    TOR_ENABLED = is_working

    tor_status_indicator = f"{Fore.GREEN}🔒 TOR ENABLED{Style.RESET_ALL}" if TOR_ENABLED else f"{Fore.RED}🔓 TOR DISABLED{Style.RESET_ALL}"

    menu = f"""
{Fore.GREEN}Available Tools:{Style.RESET_ALL}

{tor_status_indicator}

{Fore.YELLOW}1.{Style.RESET_ALL} SMS Tool {'🛡️' if TOR_ENABLED else '⚠️'}
{Fore.YELLOW}2.{Style.RESET_ALL} Tor Connection Manager
{Fore.YELLOW}3.{Style.RESET_ALL} Tor Network Settings
{Fore.YELLOW}4.{Style.RESET_ALL} Exit

{Fore.CYAN}Select an option (1-4): {Style.RESET_ALL}"""

    print(menu)


def run_sms_tool():
    """Run SMS tool with Tor awareness"""
    global TOR_ENABLED

    print(f"\n{Fore.GREEN}Launching SMS Tool...{Style.RESET_ALL}")

    # Show Tor status
    if TOR_ENABLED:
        print(f"{Fore.GREEN}🛡️ SMS will be sent through Tor network{Style.RESET_ALL}")
        is_working, tor_ip, real_ip = check_tor_connection()
        if is_working:
            print(f"🎭 Your Tor IP: {tor_ip}")
    else:
        print(f"{Fore.RED}⚠️ Warning: Tor is not enabled!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}SMS will be sent with your real IP{Style.RESET_ALL}")

        response = input(
            f"{Fore.CYAN}Enable Tor first? (y/n): {Style.RESET_ALL}").strip().lower()
        if response == 'y':
            if enable_tor_globally():
                print(f"{Fore.GREEN}✅ Tor enabled for SMS tool{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Continuing without Tor{Style.RESET_ALL}")

    try:
        # Import and run SMS tool
        # First try the original sms.py
        try:
            from sms import main as sms_main
            sms_main()
        except ImportError:
            # Fallback to sms_fallback if exists
            try:
                from sms_fallback import main as sms_main
                sms_main()
            except ImportError:
                print(f"{Fore.RED}❌ No SMS tool found!{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error in SMS tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def run_tor_tool():
    """Run the dedicated Tor connection tool"""
    print(f"\n{Fore.GREEN}Launching Tor Connection Manager...{Style.RESET_ALL}")
    try:
        from tor import main as tor_main
        tor_main()
    except ImportError as e:
        print(f"{Fore.RED}Error loading Tor tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    # Initial Tor status check
    global TOR_ENABLED
    is_working, tor_ip, real_ip = check_tor_connection()
    TOR_ENABLED = is_working

    while True:
        clear_screen()
        print_banner()
        show_menu()

        choice = input().strip()

        if choice == '1':
            run_sms_tool()
        elif choice == '2':
            run_tor_tool()
        elif choice == '3':
            tor_status_menu()
        elif choice == '4':
            # Disable Tor before exit
            disable_tor_globally()
            print(
                f"\n{Fore.GREEN}Thank you for using Linux Toolkit!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}Invalid choice! Please select 1-4{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Disable Tor on exit
        disable_tor_globally()
        print(f"\n{Fore.YELLOW}Program interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
