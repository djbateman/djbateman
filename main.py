#!/usr/bin/env python3
"""
Cisco Router Simulator
Main entry point for the router simulator application.
"""

import sys
import argparse
from cisco_router import CiscoRouter
from cli_interface import CLIInterface


def main():
    """Main function to start the router simulator."""
    parser = argparse.ArgumentParser(
        description="Cisco Router Simulator - A simple Cisco IOS CLI simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start with default hostname 'Router'
  python main.py --hostname R1      # Start with custom hostname
  python main.py --help             # Show this help message

Commands to try:
  enable                            # Enter privileged mode
  configure terminal                # Enter configuration mode
  show version                      # Display IOS version
  show ip interface brief           # Show interface status
        """
    )

    parser.add_argument(
        '--hostname',
        default='Router',
        help='Set the initial router hostname (default: Router)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Cisco Router Simulator v1.0'
    )

    args = parser.parse_args()

    # Create router instance
    router = CiscoRouter(hostname=args.hostname)

    # Create CLI interface
    cli = CLIInterface(router)

    # Start the CLI
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nRouter simulator terminated.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
