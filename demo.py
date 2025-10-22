#!/usr/bin/env python3
"""
Demo script for Cisco Router Simulator
Demonstrates various commands without requiring interactive input.
"""

from cisco_router import CiscoRouter
from cli_interface import CLIInterface


def run_demo():
    """Run a demonstration of the router simulator."""
    print("=" * 70)
    print("Cisco Router Simulator - Interactive Demo")
    print("=" * 70)
    print()

    # Create router and CLI
    router = CiscoRouter(hostname="DemoRouter")
    cli = CLIInterface(router)

    # Simulate commands
    commands = [
        ("", "User EXEC Mode - Basic commands available"),
        ("show version", "Display IOS version and system info"),
        ("enable", "Enter privileged EXEC mode"),
        ("show ip interface brief", "Show all interfaces"),
        ("configure terminal", "Enter global configuration mode"),
        ("hostname CoreRouter", "Change the hostname"),
        ("interface GigabitEthernet0/0", "Configure an interface"),
        ("description LAN Connection to Building A", "Set interface description"),
        ("ip address 192.168.1.1 255.255.255.0", "Configure IP address"),
        ("no shutdown", "Bring the interface up"),
        ("exit", "Exit interface config mode"),
        ("interface GigabitEthernet0/1", "Configure another interface"),
        ("ip address 10.0.0.1 255.255.255.0", "Configure IP address"),
        ("no shutdown", "Bring the interface up"),
        ("end", "Return to privileged EXEC mode"),
        ("show ip interface brief", "Show updated interface status"),
        ("show running-config", "Display the running configuration"),
        ("write", "Save configuration"),
    ]

    for cmd, description in commands:
        if cmd == "":
            # Header
            print("\n" + "─" * 70)
            print(f"  {description}")
            print("─" * 70)
            continue

        prompt = cli.get_prompt()
        print(f"\n{prompt} {cmd}")

        if description:
            print(f"  → {description}")

        output = cli.execute_command(cmd)
        if output:
            # Print output with slight indentation
            for line in output.split('\n'):
                print(f"  {line}")

    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nTo run the simulator interactively, use:")
    print("  python3 main.py")
    print("\nFor help within the simulator, type '?' at any prompt")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
