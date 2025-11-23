#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from typing import List, Tuple

# Try to import curses for Windows
try:
    import curses
except ImportError:
    print("❌ curses not available. Installing windows-curses...")
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', 'windows-curses'])
    import curses


class HackerToolkit:
    def __init__(self):
        self.tor_enabled = False
        self.stdscr = None
        self.current_selection = 0
        self.menu_items = [
            "SMS Bomber",
            "Tor Manager",
            "Exit"
        ]

    def init_curses(self):
        """Initialize curses with hacker theme"""
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.curs_set(0)
            return True
        except:
            return False

    def draw_banner(self):
        """Draw hacker-style banner"""
        banner = [
            "╔════════════════════════════════════════════╗",
            "║           PYTHON HACKER TOOLKIT           ║",
            "║              [ ANONYMOUS MODE ]           ║",
            "╚════════════════════════════════════════════╝"
        ]

        for i, line in enumerate(banner):
            try:
                self.stdscr.addstr(i + 2, 2, line, curses.color_pair(1))
            except:
                pass

    def draw_status(self):
        """Display current Tor status"""
        status_line = "Tor Status: "
        if self.tor_enabled:
            status_line += "[ACTIVE - ANONYMOUS]"
            color = curses.color_pair(1)
        else:
            status_line += "[INACTIVE - VISIBLE]"
            color = curses.color_pair(3)

        try:
            self.stdscr.addstr(8, 2, status_line, color)
        except:
            pass

    def draw_menu(self):
        """Draw the main menu"""
        try:
            self.stdscr.addstr(10, 2, "SELECT TOOL:", curses.color_pair(1))

            for i, item in enumerate(self.menu_items):
                if i == self.current_selection:
                    self.stdscr.addstr(
                        12 + i, 4, f"> {item}", curses.color_pair(2))
                else:
                    self.stdscr.addstr(
                        12 + i, 4, f"  {item}", curses.color_pair(1))
        except:
            pass

    def run_sms_bomber(self):
        """Run SMS Bomber with current Tor setting"""
        self.stdscr.clear()
        self.stdscr.addstr(2, 2, "🚀 LAUNCHING SMS BOMBER...",
                           curses.color_pair(1))
        self.stdscr.refresh()

        # Set environment for Tor if enabled
        env = os.environ.copy()
        if self.tor_enabled:
            env['ALL_PROXY'] = 'socks5://127.0.0.1:9050'
            self.stdscr.addstr(
                4, 2, "🔒 USING TOR NETWORK - ANONYMOUS MODE", curses.color_pair(1))
        else:
            self.stdscr.addstr(
                4, 2, "⚠️  DIRECT CONNECTION - NO ANONYMITY", curses.color_pair(3))

        self.stdscr.addstr(6, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

        try:
            # Run SMS Bomber
            import sms
        except Exception as e:
            self.stdscr.addstr(8, 2, f"❌ Error: {e}", curses.color_pair(3))
            self.stdscr.addstr(10, 2, "Press any key to return...")
            self.stdscr.refresh()
            self.stdscr.getch()

    def tor_manager(self):
        """Tor management interface"""
        while True:
            self.stdscr.clear()
            self.draw_banner()

            self.stdscr.addstr(8, 2, "🔧 TOR MANAGER", curses.color_pair(1))
            self.stdscr.addstr(10, 2, "1. Connect to Tor")
            self.stdscr.addstr(11, 2, "2. Disconnect from Tor")
            self.stdscr.addstr(12, 2, "3. Check Tor Status")
            self.stdscr.addstr(13, 2, "4. Back to Main Menu")

            self.stdscr.addstr(
                15, 2, f"Current Status: {'ACTIVE' if self.tor_enabled else 'INACTIVE'}")

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == ord('1'):
                self.connect_tor()
            elif key == ord('2'):
                self.disconnect_tor()
            elif key == ord('3'):
                self.check_tor_status()
            elif key == ord('4'):
                break

    def connect_tor(self):
        """Connect to Tor network"""
        self.stdscr.clear()
        self.draw_banner()

        self.stdscr.addstr(
            8, 2, "🔄 CONNECTING TO TOR NETWORK...", curses.color_pair(1))
        self.stdscr.refresh()

        try:
            import requests
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }

            response = session.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                self.tor_enabled = True
                ip_info = response.json()
                self.stdscr.addstr(
                    10, 2, f"✅ TOR CONNECTED SUCCESSFULLY!", curses.color_pair(1))
                self.stdscr.addstr(
                    11, 2, f"🌐 Your Tor IP: {ip_info.get('origin', 'Unknown')}")
            else:
                self.stdscr.addstr(
                    10, 2, "❌ Failed to connect to Tor", curses.color_pair(3))

        except Exception as e:
            self.stdscr.addstr(
                10, 2, f"❌ Tor connection failed: {e}", curses.color_pair(3))
            self.stdscr.addstr(
                12, 2, "Make sure Tor is installed and running on port 9050")

        self.stdscr.addstr(14, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

    def disconnect_tor(self):
        """Disconnect from Tor"""
        self.tor_enabled = False
        self.stdscr.clear()
        self.draw_banner()
        self.stdscr.addstr(8, 2, "✅ DISCONNECTED FROM TOR",
                           curses.color_pair(1))
        self.stdscr.addstr(10, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

    def check_tor_status(self):
        """Check current Tor status and IP"""
        self.stdscr.clear()
        self.draw_banner()

        self.stdscr.addstr(
            8, 2, "🔍 CHECKING NETWORK STATUS...", curses.color_pair(1))
        self.stdscr.refresh()

        try:
            import requests

            if self.tor_enabled:
                session = requests.Session()
                session.proxies = {
                    'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'
                }
                response = session.get('http://httpbin.org/ip', timeout=10)
                ip_info = response.json()

                self.stdscr.addstr(10, 2, "✅ TOR ACTIVE", curses.color_pair(1))
                self.stdscr.addstr(
                    11, 2, f"🌐 Tor IP: {ip_info.get('origin', 'Unknown')}")
            else:
                response = requests.get('http://httpbin.org/ip', timeout=10)
                ip_info = response.json()

                self.stdscr.addstr(
                    10, 2, "⚠️  DIRECT CONNECTION", curses.color_pair(3))
                self.stdscr.addstr(
                    11, 2, f"🌐 Your Real IP: {ip_info.get('origin', 'Unknown')}")

        except Exception as e:
            self.stdscr.addstr(
                10, 2, f"❌ Error checking status: {e}", curses.color_pair(3))

        self.stdscr.addstr(14, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

    def main_loop(self, stdscr):
        """Main application loop"""
        self.stdscr = stdscr
        if not self.init_curses():
            self.stdscr.addstr(0, 0, "⚠️  Color support not available")

        while True:
            self.stdscr.clear()
            self.draw_banner()
            self.draw_status()
            self.draw_menu()

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.current_selection = (
                    self.current_selection - 1) % len(self.menu_items)
            elif key == curses.KEY_DOWN:
                self.current_selection = (
                    self.current_selection + 1) % len(self.menu_items)
            elif key == ord('\n') or key == ord(' '):
                if self.current_selection == 0:
                    self.run_sms_bomber()
                elif self.current_selection == 1:
                    self.tor_manager()
                elif self.current_selection == 2:
                    break

    def run(self):
        """Start the application"""
        try:
            curses.wrapper(self.main_loop)
            print("\n👋 Goodbye! Stay anonymous!")
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Stay anonymous!")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    toolkit = HackerToolkit()
    toolkit.run()
