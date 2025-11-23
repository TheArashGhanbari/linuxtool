#!/usr/bin/env python3
import os
import subprocess
import pwd
import grp
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from colorama import Fore, Style

console = Console()


def security_audit_tool():
    """Security Audit Tool"""

    console.print(Panel.fit(
        "[bold cyan]Security Audit Tool[/bold cyan]",
        border_style="cyan"
    ))

    while True:
        console.print(f"\n{Fore.CYAN}=== Security Audit ==={Style.RESET_ALL}")
        console.print(
            f"{Fore.GREEN}[1]{Style.RESET_ALL} File Permissions Check")
        console.print(f"{Fore.GREEN}[2]{Style.RESET_ALL} User Account Audit")
        console.print(f"{Fore.GREEN}[3]{Style.RESET_ALL} SSH Security Check")
        console.print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Firewall Status")
        console.print(f"{Fore.GREEN}[5]{Style.RESET_ALL} SUID/SGID Files")
        console.print(f"{Fore.RED}[0]{Style.RESET_ALL} Return to Main Menu")

        choice = console.input(
            f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")

        if choice == "1":
            file_permissions_check()
        elif choice == "2":
            user_account_audit()
        elif choice == "3":
            ssh_security_check()
        elif choice == "4":
            firewall_status()
        elif choice == "5":
            suid_sgid_files()
        elif choice == "0":
            break
        else:
            console.print(f"{Fore.RED}❌ Invalid option!{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def file_permissions_check():
    console.print(
        f"\n{Fore.YELLOW}Checking critical file permissions...{Style.RESET_ALL}")

    critical_files = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        "/etc/ssh/sshd_config",
        "/etc/hosts",
        "/etc/hosts.allow",
        "/etc/hosts.deny"
    ]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Permissions", style="green")
    table.add_column("Owner", style="yellow")
    table.add_column("Group", style="blue")
    table.add_column("Status", style="red")

    for file_path in critical_files:
        if os.path.exists(file_path):
            try:
                stat_info = os.stat(file_path)
                permissions = oct(stat_info.st_mode)[-3:]
                owner = pwd.getpwuid(stat_info.st_uid).pw_name
                group = grp.getgrgid(stat_info.st_gid).gr_name

                # Check if permissions are secure
                status = "✅ Secure"
                if file_path == "/etc/shadow" and permissions != "000":
                    status = "⚠️  Warning"
                elif file_path == "/etc/passwd" and int(permissions) > 644:
                    status = "⚠️  Warning"
                elif file_path == "/etc/sudoers" and int(permissions) > 440:
                    status = "⚠️  Warning"

                table.add_row(file_path, permissions, owner, group, status)

            except Exception as e:
                table.add_row(file_path, "N/A", "N/A", "N/A", f"❌ Error: {e}")
        else:
            table.add_row(file_path, "N/A", "N/A", "N/A", "❌ Not found")

    console.print(table)


def user_account_audit():
    console.print(f"\n{Fore.YELLOW}Auditing user accounts...{Style.RESET_ALL}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Username", style="cyan")
    table.add_column("UID", style="green")
    table.add_column("GID", style="yellow")
    table.add_column("Home Directory", style="blue")
    table.add_column("Shell", style="magenta")
    table.add_column("Status", style="red")

    try:
        for user in pwd.getpwall():
            status = "✅ Normal"
            if user.pw_uid == 0:
                status = "👑 Root"
            elif user.pw_uid < 1000:
                status = "⚙️  System"
            elif user.pw_shell in ["/bin/false", "/usr/sbin/nologin"]:
                status = "🔒 Locked"

            table.add_row(
                user.pw_name,
                str(user.pw_uid),
                str(user.pw_gid),
                user.pw_dir,
                user.pw_shell,
                status
            )

    except Exception as e:
        console.print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    console.print(table)


def ssh_security_check():
    console.print(
        f"\n{Fore.YELLOW}Checking SSH configuration...{Style.RESET_ALL}")

    ssh_config_path = "/etc/ssh/sshd_config"
    checks = []

    if os.path.exists(ssh_config_path):
        try:
            with open(ssh_config_path, 'r') as f:
                content = f.read().lower()

            # Check for common security settings
            checks.append(("Password Authentication",
                          "passwordauthentication no" in content, "Should be disabled"))
            checks.append(
                ("Root Login", "permitrootlogin no" in content, "Should be disabled"))
            checks.append(
                ("Empty Passwords", "permitemptypasswords no" in content, "Should be disabled"))
            checks.append(("X11 Forwarding", "x11forwarding no" in content,
                          "Should be disabled if not needed"))
            checks.append(("Protocol", "protocol 2" in content,
                          "Should use SSHv2 only"))

        except Exception as e:
            console.print(
                f"{Fore.RED}❌ Error reading SSH config: {e}{Style.RESET_ALL}")
            return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Recommendation", style="yellow")

    for check_name, is_secure, recommendation in checks:
        status = "✅ Secure" if is_secure else "❌ Insecure"
        table.add_row(check_name, status, recommendation)

    console.print(table)


def firewall_status():
    console.print(
        f"\n{Fore.YELLOW}Checking firewall status...{Style.RESET_ALL}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Firewall", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Service", style="yellow")

    # Check common firewall services
    firewall_services = [
        ("iptables", "iptables"),
        ("ufw", "ufw"),
        ("firewalld", "firewalld")
    ]

    for fw_name, service_name in firewall_services:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            status = "✅ Active" if result.stdout.strip() == "active" else "❌ Inactive"
            table.add_row(fw_name, status, service_name)
        except Exception as e:
            table.add_row(fw_name, "❌ Error", str(e))

    console.print(table)


def suid_sgid_files():
    console.print(
        f"\n{Fore.YELLOW}Finding SUID/SGID files...{Style.RESET_ALL}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Permissions", style="green")
    table.add_column("Owner", style="yellow")
    table.add_column("Size", style="blue")

    try:
        # Find SUID/SGID files in common directories
        result = subprocess.run(
            ['find', '/bin', '/usr/bin', '/sbin', '/usr/sbin',
                '-type', 'f', '-perm', '-4000,-2000', '-ls'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 10:
                        permissions = parts[2]
                        owner = parts[4]
                        size = parts[6]
                        filename = parts[10] if len(parts) > 10 else "Unknown"
                        table.add_row(filename, permissions, owner, size)

        if not table.rows:
            console.print(
                f"{Fore.GREEN}✅ No unusual SUID/SGID files found{Style.RESET_ALL}")
        else:
            console.print(table)

    except Exception as e:
        console.print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    security_audit_tool()
