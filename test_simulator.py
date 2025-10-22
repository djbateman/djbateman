#!/usr/bin/env python3
"""
Test script for Cisco Router Simulator
Validates core functionality without user interaction.
"""

import sys
from cisco_router import CiscoRouter
from cli_interface import CLIInterface, Mode
from commands import CommandHandler


def test_router_creation():
    """Test basic router creation and initialization."""
    print("Testing router creation...")
    router = CiscoRouter(hostname="TestRouter")
    assert router.hostname == "TestRouter"
    assert len(router.interfaces) == 3
    print("✓ Router created successfully")


def test_interface_configuration():
    """Test interface configuration."""
    print("\nTesting interface configuration...")
    router = CiscoRouter()

    # Configure IP address
    router.configure_interface(
        "GigabitEthernet0/0",
        ip_address="192.168.1.1",
        subnet_mask="255.255.255.0"
    )

    assert router.interfaces["GigabitEthernet0/0"]["ip_address"] == "192.168.1.1"
    assert router.interfaces["GigabitEthernet0/0"]["subnet_mask"] == "255.255.255.0"
    print("✓ Interface configured successfully")


def test_interface_status():
    """Test interface shutdown/no shutdown."""
    print("\nTesting interface status control...")
    router = CiscoRouter()

    # Initially, interfaces should be administratively down
    assert router.interfaces["GigabitEthernet0/0"]["status"] == "administratively down"

    # Bring up the interface
    router.no_shutdown_interface("GigabitEthernet0/0")
    assert router.interfaces["GigabitEthernet0/0"]["status"] == "up"

    # Shutdown the interface
    router.shutdown_interface("GigabitEthernet0/0")
    assert router.interfaces["GigabitEthernet0/0"]["status"] == "administratively down"
    print("✓ Interface status control works")


def test_hostname_change():
    """Test hostname change."""
    print("\nTesting hostname change...")
    router = CiscoRouter()
    router.set_hostname("NewRouter")
    assert router.hostname == "NewRouter"
    assert router.running_config["hostname"] == "NewRouter"
    print("✓ Hostname changed successfully")


def test_enable_password():
    """Test enable password functionality."""
    print("\nTesting enable password...")
    router = CiscoRouter()

    # Set password
    router.set_enable_password("mypassword")
    assert router.verify_enable_password("mypassword") == True
    assert router.verify_enable_password("wrongpassword") == False

    # Set secret (takes precedence)
    router.set_enable_password("mysecret", secret=True)
    assert router.verify_enable_password("mysecret") == True
    assert router.verify_enable_password("mypassword") == False
    print("✓ Enable password works correctly")


def test_config_save():
    """Test configuration save."""
    print("\nTesting configuration save...")
    router = CiscoRouter()

    # Make changes to running config
    router.set_hostname("SavedRouter")
    router.configure_interface("GigabitEthernet0/0", ip_address="10.0.0.1")

    # Save configuration
    router.save_config()

    assert router.startup_config["hostname"] == "SavedRouter"
    print("✓ Configuration saved successfully")


def test_show_commands():
    """Test show commands."""
    print("\nTesting show commands...")
    router = CiscoRouter(hostname="ShowTestRouter")
    handler = CommandHandler(router)

    # Test show version
    version_output = handler.show_version()
    assert "ShowTestRouter" in version_output
    assert router.ios_version in version_output

    # Configure an interface first
    router.configure_interface(
        "GigabitEthernet0/0",
        ip_address="192.168.1.1",
        subnet_mask="255.255.255.0"
    )
    router.no_shutdown_interface("GigabitEthernet0/0")

    # Test show ip interface brief
    brief_output = handler.show_ip_interface_brief()
    assert "GigabitEthernet0/0" in brief_output
    assert "192.168.1.1" in brief_output

    # Test show running-config
    running_config = handler.show_running_config()
    assert "ShowTestRouter" in running_config
    assert "interface GigabitEthernet0/0" in running_config

    print("✓ Show commands work correctly")


def test_cli_modes():
    """Test CLI mode transitions."""
    print("\nTesting CLI modes...")
    router = CiscoRouter()
    cli = CLIInterface(router)

    # Initial mode should be user EXEC
    assert cli.mode == Mode.USER_EXEC
    assert cli.get_prompt() == "Router>"

    # Test mode transitions
    cli.mode = Mode.PRIVILEGED_EXEC
    assert cli.get_prompt() == "Router#"

    cli.mode = Mode.GLOBAL_CONFIG
    assert cli.get_prompt() == "Router(config)#"

    cli.mode = Mode.INTERFACE_CONFIG
    assert cli.get_prompt() == "Router(config-if)#"

    print("✓ CLI modes work correctly")


def test_command_parsing():
    """Test command parsing."""
    print("\nTesting command parsing...")
    router = CiscoRouter()
    cli = CLIInterface(router)

    # Test simple command parsing
    cmd, args = cli.parse_command("show version")
    assert cmd == "show"
    assert args == ["version"]

    cmd, args = cli.parse_command("interface GigabitEthernet0/0")
    assert cmd == "interface"
    assert args == ["GigabitEthernet0/0"]

    print("✓ Command parsing works correctly")


def test_interface_name_normalization():
    """Test interface name normalization."""
    print("\nTesting interface name normalization...")
    router = CiscoRouter()
    cli = CLIInterface(router)

    # Test abbreviations
    assert "GigabitEthernet0/0" in cli.normalize_interface_name("gi0/0")
    assert "GigabitEthernet0/1" in cli.normalize_interface_name("gig0/1")

    print("✓ Interface name normalization works")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Cisco Router Simulator - Test Suite")
    print("=" * 60)

    try:
        test_router_creation()
        test_interface_configuration()
        test_interface_status()
        test_hostname_change()
        test_enable_password()
        test_config_save()
        test_show_commands()
        test_cli_modes()
        test_command_parsing()
        test_interface_name_normalization()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
