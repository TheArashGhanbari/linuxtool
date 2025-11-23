#!/usr/bin/env python3
import os
import sys
import subprocess
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored text
init()


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                   Linux Security Toolkit                    ║
║                     Terminal Interface                      ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def print_menu():
    menu = f"""
{Fore.YELLOW}Available Tools:{Style.RESET_ALL}

{Fore.GREEN}[1]{Style.RESET_ALL} SMS Analysis Tool
{Fore.GREEN}[2]{Style.RESET_ALL} Tor Management Tool
{Fore.RED}[0]{Style.RESET_ALL} Exit

"""
    print(menu)


def run_sms_tool():
    print(f"\n{Fore.YELLOW}Launching SMS Analysis Tool...{Style.RESET_ALL}")
    try:
        # Run the sms.py tool
        subprocess.run([sys.executable, "sms.py"])
    except Exception as e:
        print(f"{Fore.RED}Error running SMS tool: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


def run_tor_tool():
    print(f"\n{Fore.YELLOW}Launching Tor Management Tool...{Style.RESET_ALL}")
    try:
        from tor_manager import tor_tool
        tor_tool()
    except ImportError as e:
        print(f"{Fore.RED}Error: Required module not found: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}To install dependencies use:{Style.RESET_ALL}")
        print("pip install requests stem socks")
    except Exception as e:
        print(f"{Fore.RED}Error running Tor tool: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()

        choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")

        if choice == "1":
            run_sms_tool()
        elif choice == "2":
            run_tor_tool()
        elif choice == "0":
            print(
                f"\n{Fore.GREEN}Thank you for using Linux Security Toolkit!{Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.RED}Invalid option! Please try again.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
