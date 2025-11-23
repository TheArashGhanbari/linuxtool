#!/usr/bin/env python3
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════╗
║           {Fore.YELLOW}LINUX TOOLKIT{Fore.CYAN}                   ║
║              {Fore.WHITE}Multi-Tool Platform{Fore.CYAN}           ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def show_menu():
    menu = f"""
{Fore.GREEN}Available Tools:{Style.RESET_ALL}

{Fore.YELLOW}1.{Style.RESET_ALL} SMS Tool
{Fore.YELLOW}2.{Style.RESET_ALL} Tor Connection Tool
{Fore.YELLOW}3.{Style.RESET_ALL} Exit

{Fore.CYAN}Select an option (1-3): {Style.RESET_ALL}"""

    print(menu)


def run_sms_tool():
    print(f"\n{Fore.GREEN}Launching SMS Tool...{Style.RESET_ALL}")
    try:
        # Check if sms.py exists and is readable
        if not os.path.exists("sms.py"):
            print(f"{Fore.RED}Error: sms.py file not found{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return

        # Import and run SMS tool
        from sms import main as sms_main
        sms_main()
    except ImportError as e:
        print(f"{Fore.RED}Error loading SMS tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error in SMS tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def run_tor_tool():
    print(f"\n{Fore.GREEN}Launching Tor Tool...{Style.RESET_ALL}")
    try:
        # Check if tor.py exists and is readable
        if not os.path.exists("tor.py"):
            print(f"{Fore.RED}Error: tor.py file not found{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return

        # Import and run Tor tool
        from tor import main as tor_main
        tor_main()
    except ImportError as e:
        print(f"{Fore.RED}Error loading Tor tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error in Tor tool: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    while True:
        clear_screen()
        print_banner()
        show_menu()

        try:
            choice = input().strip()

            if choice == '1':
                run_sms_tool()
            elif choice == '2':
                run_tor_tool()
            elif choice == '3':
                print(
                    f"\n{Fore.GREEN}Thank you for using Linux Toolkit!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(
                    f"\n{Fore.RED}Invalid choice! Please select 1-3{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
            time.sleep(1)
        except Exception as e:
            print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
