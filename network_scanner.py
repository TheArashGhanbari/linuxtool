#!/usr/bin/env python3
import socket
import subprocess
import platform
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from colorama import Fore, Style

console = Console()


def network_scanner_tool():
    """Network Scanner Tool"""

    console.print(Panel.fit(
        "[bold cyan]Network Scanner Tool[/bold cyan]",
        border_style="cyan"
    ))

    while True:
        console.print(f"\n{Fore.CYAN}=== Network Scanner ==={Style.RESET_ALL}")
        console.print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Port Scanner")
        console.print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Ping Sweep")
        console.print(f"{Fore.GREEN}[3]{Style.RESET_ALL} DNS Lookup")
        console.print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Network Interfaces")
        console.print(f"{Fore.RED}[0]{Style.RESET_ALL} Return to Main Menu")

        choice = console.input(
            f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")

        if choice == "1":
            port_scanner()
        elif choice == "2":
            ping_sweep()
        elif choice == "3":
            dns_lookup()
        elif choice == "4":
            network_interfaces()
        elif choice == "0":
            break
        else:
            console.print(f"{Fore.RED}❌ Invalid option!{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def port_scanner():
    target = console.input(
        f"{Fore.CYAN}Enter target IP or hostname: {Style.RESET_ALL}")
    ports = console.input(
        f"{Fore.CYAN}Enter ports to scan (e.g., 80,443 or 1-1000): {Style.RESET_ALL}")

    console.print(f"\n{Fore.YELLOW}Scanning {target}...{Style.RESET_ALL}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Service", style="yellow")

    try:
        if '-' in ports:
            start_port, end_port = map(int, ports.split('-'))
            ports_range = range(start_port, end_port + 1)
        else:
            ports_range = map(int, ports.split(','))

        for port in ports_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                table.add_row(str(port), "✅ Open", service)

        console.print(table)

    except Exception as e:
        console.print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")


def ping_sweep():
    network = console.input(
        f"{Fore.CYAN}Enter network (e.g., 192.168.1.0/24): {Style.RESET_ALL}")

    console.print(
        f"\n{Fore.YELLOW}Pinging network {network}...{Style.RESET_ALL}")

    # Simple implementation - in real tool you'd use python-nmap or similar
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("IP Address", style="cyan")
    table.add_column("Status", style="green")

    # This is a basic example - you'd need to implement proper network scanning
    console.print(
        f"{Fore.YELLOW}Note: Full ping sweep requires root privileges and proper implementation{Style.RESET_ALL}")


def dns_lookup():
    hostname = console.input(f"{Fore.CYAN}Enter hostname: {Style.RESET_ALL}")

    try:
        console.print(
            f"\n{Fore.YELLOW}DNS Lookup for {hostname}:{Style.RESET_ALL}")

        # Get IP address
        ip_address = socket.gethostbyname(hostname)
        console.print(f"{Fore.GREEN}IP Address: {ip_address}{Style.RESET_ALL}")

        # Get all IP addresses
        all_ips = socket.getaddrinfo(hostname, None)
        unique_ips = set(ip[4][0] for ip in all_ips)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("IP Addresses", style="cyan")

        for ip in unique_ips:
            table.add_row(ip)

        console.print(table)

    except Exception as e:
        console.print(f"{Fore.RED}❌ DNS Lookup failed: {e}{Style.RESET_ALL}")


def network_interfaces():
    console.print(f"\n{Fore.YELLOW}Network Interfaces:{Style.RESET_ALL}")

    try:
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(result.stdout)
        else:
            # Fallback for different systems
            result = subprocess.run(
                ['ifconfig'], capture_output=True, text=True)
            if result.returncode == 0:
                console.print(result.stdout)
            else:
                console.print(
                    f"{Fore.RED}❌ Could not retrieve network interfaces{Style.RESET_ALL}")
    except Exception as e:
        console.print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    network_scanner_tool()
