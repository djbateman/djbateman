#!/usr/bin/env python3
"""Quick test showing specific commands"""

from cisco_router import CiscoRouter
from cli_interface import CLIInterface

router = CiscoRouter(hostname="Lab-Router")
cli = CLIInterface(router)

print("\n" + "="*60)
print("Testing: show version command")
print("="*60)
print(cli.execute_command("show version"))

print("\n" + "="*60)
print("Testing: Configure interface and show details")
print("="*60)
cli.execute_command("enable")
cli.execute_command("configure terminal")
cli.execute_command("interface GigabitEthernet0/0")
cli.execute_command("ip address 172.16.10.1 255.255.255.0")
cli.execute_command("description Connected to Server Farm")
cli.execute_command("no shutdown")
cli.execute_command("end")

print("\nCurrent prompt:", cli.get_prompt())
print("\n" + cli.execute_command("show interfaces GigabitEthernet0/0"))

print("\n" + "="*60)
print("Testing: show ip route")
print("="*60)
print(cli.execute_command("show ip route"))

print("\n" + "="*60)
print("All commands work! Try 'python3 main.py' for interactive mode")
print("="*60)
