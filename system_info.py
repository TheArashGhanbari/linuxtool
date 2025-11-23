#!/usr/bin/env python3
import platform
import psutil
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from colorama import Fore, Style

console = Console()


def system_info_tool():
    """System Information Tool"""

    console.print(Panel.fit(
        "[bold cyan]System Information Tool[/bold cyan]",
        border_style="cyan"
    ))

    while True:
        console.print(
            f"\n{Fore.CYAN}=== System Information ==={Style.RESET_ALL}")
        console.print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Basic System Info")
        console.print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Hardware Information")
        console.print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Network Information")
        console.print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Disk Usage")
        console.print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Running Processes")
        console.print(f"{Fore.RED}[0]{Style.RESET_ALL} Return to Main Menu")

        choice = console.input(
            f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")

        if choice == "1":
            basic_system_info()
        elif choice == "2":
            hardware_info()
        elif choice == "3":
            network_info()
        elif choice == "4":
            disk_usage()
        elif choice == "5":
            running_processes()
        elif choice == "0":
            break
        else:
            console.print(f"{Fore.RED}❌ Invalid option!{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def basic_system_info():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    # System information
    table.add_row("System", platform.system())
    table.add_row("Node Name", platform.node())
    table.add_row("Release", platform.release())
    table.add_row("Version", platform.version())
    table.add_row("Machine", platform.machine())
    table.add_row("Processor", platform.processor())
    table.add_row("Boot Time", datetime.fromtimestamp(
        psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

    console.print(table)


def hardware_info():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Hardware Component", style="cyan")
    table.add_column("Information", style="green")

    # CPU information
    cpu_percent = psutil.cpu_percent(interval=1)
    table.add_row("CPU Cores", str(psutil.cpu_count()))
    table.add_row("CPU Usage", f"{cpu_percent}%")
    table.add_row("CPU Frequency", f"{psutil.cpu_freq().current:.2f} MHz")

    # Memory information
    memory = psutil.virtual_memory()
    table.add_row("Total Memory", f"{memory.total / (1024**3):.2f} GB")
    table.add_row("Available Memory", f"{memory.available / (1024**3):.2f} GB")
    table.add_row("Memory Usage", f"{memory.percent}%")

    # Swap memory
    swap = psutil.swap_memory()
    table.add_row("Swap Total", f"{swap.total / (1024**3):.2f} GB")
    table.add_row("Swap Used", f"{swap.used / (1024**3):.2f} GB")

    console.print(table)


def network_info():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Interface", style="cyan")
    table.add_column("IP Address", style="green")
    table.add_column("Netmask", style="yellow")
    table.add_column("Broadcast", style="blue")

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    table.add_row(interface, addr.address,
                                  addr.netmask, addr.broadcast or "N/A")

    except Exception as e:
        console.print(
            f"{Fore.RED}❌ Error getting network info: {e}{Style.RESET_ALL}")

    console.print(table)


def disk_usage():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Device", style="cyan")
    table.add_column("Mountpoint", style="green")
    table.add_column("Total Size", style="yellow")
    table.add_column("Used", style="red")
    table.add_column("Free", style="blue")
    table.add_column("Usage %", style="magenta")

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            table.add_row(
                partition.device,
                partition.mountpoint,
                f"{usage.total / (1024**3):.1f} GB",
                f"{usage.used / (1024**3):.1f} GB",
                f"{usage.free / (1024**3):.1f} GB",
                f"{usage.percent}%"
            )
        except PermissionError:
            continue

    console.print(table)


def running_processes():
    console.print(
        f"\n{Fore.YELLOW}Top 10 processes by CPU usage:{Style.RESET_ALL}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("PID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("CPU %", style="yellow")
    table.add_column("Memory %", style="red")
    table.add_column("Status", style="blue")

    # Get top 10 processes by CPU usage
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort by CPU usage and take top 10
    processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)

    for proc in processes[:10]:
        table.add_row(
            str(proc['pid']),
            proc['name'],
            f"{proc['cpu_percent'] or 0:.1f}%",
            f"{proc['memory_percent'] or 0:.1f}%",
            proc['status']
        )

    console.print(table)


if __name__ == "__main__":
    system_info_tool()
