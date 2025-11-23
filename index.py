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
{Fore.GREEN}[3]{Style.RESET_ALL} Network Scanner
{Fore.GREEN}[4]{Style.RESET_ALL} System Information
{Fore.GREEN}[5]{Style.RESET_ALL} Security Audit
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


def run_network_scanner():
    print(f"\n{Fore.YELLOW}Launching Network Scanner...{Style.RESET_ALL}")
    try:
        from network_scanner import network_scanner_tool
        network_scanner_tool()
    except ImportError as e:
        print(f"{Fore.RED}Error: Required module not found: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error running Network Scanner: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


def run_system_info():
    print(f"\n{Fore.YELLOW}Launching System Information Tool...{Style.RESET_ALL}")
    try:
        from system_info import system_info_tool
        system_info_tool()
    except ImportError as e:
        print(f"{Fore.RED}Error: Required module not found: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error running System Information Tool: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


def run_security_audit():
    print(f"\n{Fore.YELLOW}Launching Security Audit Tool...{Style.RESET_ALL}")
    try:
        from security_audit import security_audit_tool
        security_audit_tool()
    except ImportError as e:
        print(f"{Fore.RED}Error: Required module not found: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error running Security Audit Tool: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'colorama',
        'requests',
        'stem',
        'Crypto',
        'rich'
    ]

    missing_modules = []
    for module in required_modules:
        try:
            if module == 'Crypto':
                __import__('Crypto.Cipher')
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print(
            f"\n{Fore.RED}❌ Missing dependencies: {', '.join(missing_modules)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please run: ./install.sh{Style.RESET_ALL}")
        return False
    return True


def main():
    # Check dependencies on startup
    if not check_dependencies():
        print(f"\n{Fore.RED}Some tools may not work properly.{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue anyway...{Style.RESET_ALL}")

    while True:
        clear_screen()
        print_banner()
        print_menu()

        choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")

        if choice == "1":
            run_sms_tool()
        elif choice == "2":
            run_tor_tool()
        elif choice == "3":
            run_network_scanner()
        elif choice == "4":
            run_system_info()
        elif choice == "5":
            run_security_audit()
        elif choice == "0":
            print(
                f"\n{Fore.GREEN}Thank you for using Linux Security Toolkit!{Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.RED}Invalid option! Please try again.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
