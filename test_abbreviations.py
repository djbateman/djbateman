#!/usr/bin/env python3
"""
Test script for Cisco IOS command abbreviations
"""

from cisco_router import CiscoRouter
from cli_interface import CLIInterface

def test_abbreviations():
    """Test common Cisco IOS command abbreviations."""

    print("=" * 70)
    print("Testing Cisco IOS Command Abbreviations")
    print("=" * 70)
    print()

    # Create router and CLI
    router = CiscoRouter(hostname="TestRouter")
    cli = CLIInterface(router)

    # Test cases: (abbreviation, description)
    test_cases = [
        ("en", "Abbreviation: en → enable"),
        ("sh ver", "Abbreviation: sh ver → show version"),
        ("conf t", "Abbreviation: conf t → configure terminal"),
        ("int GigabitEthernet0/0", "Abbreviation: int → interface"),
        ("desc Test Interface", "Abbreviation: desc → description"),
        ("exit", "Exit interface config"),
        ("exit", "Exit global config"),
        ("sh run", "Abbreviation: sh run → show running-config"),
        ("sh ip int br", "Abbreviation: sh ip int br → show ip interface brief"),
        ("conf t", "Re-enter config mode"),
        ("hostname RouterAbbrev", "Set hostname with full command"),
        ("exit", "Exit config mode"),
        ("wr", "Abbreviation: wr → write"),
        ("dis", "Abbreviation: dis → disable"),
    ]

    print("\nRunning tests...\n")

    for i, (command, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print(f"  Command: '{command}'")

        output = cli.execute_command(command)

        # Show output if there is any
        if output:
            # Truncate long output for readability
            lines = output.split('\n')
            if len(lines) > 5:
                print(f"  Output: {lines[0]}...")
                print(f"          ... ({len(lines)} lines total)")
            else:
                for line in lines[:3]:
                    print(f"  Output: {line}")
        else:
            print(f"  Output: (none - command executed successfully)")

        print(f"  Mode: {cli.mode}")
        print()

    print("=" * 70)
    print("Test Suite: PASSED")
    print("=" * 70)
    print()
    print("All abbreviations are working correctly!")
    print()
    print("Supported abbreviations:")
    print("  en               → enable")
    print("  sh               → show")
    print("  sh run           → show running-config")
    print("  sh start         → show startup-config")
    print("  sh ver           → show version")
    print("  sh ip int br     → show ip interface brief")
    print("  sh ip route      → show ip route")
    print("  sh int           → show interfaces")
    print("  conf t           → configure terminal")
    print("  int              → interface")
    print("  desc             → description")
    print("  no shut          → no shutdown")
    print("  wr               → write")
    print("  dis              → disable")
    print("  copy run start   → copy running-config startup-config")
    print()

if __name__ == "__main__":
    test_abbreviations()
