"""
Cisco Router Simulator - Core Router Class
Simulates a Cisco IOS router with configuration and state management.
"""

import time
from typing import Dict, List, Optional
from datetime import datetime


class CiscoRouter:
    """Represents a Cisco router with IOS-like functionality."""

    def __init__(self, hostname: str = "Router"):
        self.hostname = hostname
        self.running_config = self._default_config()
        self.startup_config = self._default_config()
        self.interfaces = self._initialize_interfaces()
        self.routing_table = []
        self.enable_password = "cisco"
        self.enable_secret = None
        self.uptime = time.time()
        self.ios_version = "15.1(4)M10"
        self.model = "CISCO2911/K9"

    def _default_config(self) -> Dict:
        """Returns default router configuration."""
        return {
            "hostname": self.hostname,
            "enable_password": None,
            "enable_secret": None,
            "interfaces": {},
            "routes": [],
            "banner": None,
            "line_vty": {
                "password": None,
                "login": False
            },
            "line_console": {
                "password": None,
                "login": False
            }
        }

    def _initialize_interfaces(self) -> Dict:
        """Initialize router interfaces."""
        return {
            "GigabitEthernet0/0": {
                "status": "administratively down",
                "protocol": "down",
                "ip_address": None,
                "subnet_mask": None,
                "description": None,
                "mac_address": "0000.0c00.0001"
            },
            "GigabitEthernet0/1": {
                "status": "administratively down",
                "protocol": "down",
                "ip_address": None,
                "subnet_mask": None,
                "description": None,
                "mac_address": "0000.0c00.0002"
            },
            "Serial0/0/0": {
                "status": "administratively down",
                "protocol": "down",
                "ip_address": None,
                "subnet_mask": None,
                "description": None,
                "clock_rate": None
            }
        }

    def get_uptime(self) -> str:
        """Calculate and return router uptime."""
        elapsed = int(time.time() - self.uptime)
        days = elapsed // 86400
        hours = (elapsed % 86400) // 3600
        minutes = (elapsed % 3600) // 60

        if days > 0:
            return f"{days} days, {hours} hours, {minutes} minutes"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes"
        else:
            return f"{minutes} minutes"

    def set_hostname(self, hostname: str):
        """Set router hostname."""
        self.hostname = hostname
        self.running_config["hostname"] = hostname

    def set_enable_password(self, password: str, secret: bool = False):
        """Set enable password or secret."""
        if secret:
            self.enable_secret = password
            self.running_config["enable_secret"] = password
        else:
            self.enable_password = password
            self.running_config["enable_password"] = password

    def verify_enable_password(self, password: str) -> bool:
        """Verify enable mode password."""
        # Secret takes precedence over password
        if self.enable_secret:
            return password == self.enable_secret
        return password == self.enable_password

    def configure_interface(self, interface: str, **kwargs):
        """Configure an interface with given parameters."""
        if interface not in self.interfaces:
            raise ValueError(f"Interface {interface} does not exist")

        for key, value in kwargs.items():
            self.interfaces[interface][key] = value

        # Update running config
        self.running_config["interfaces"][interface] = self.interfaces[interface].copy()

    def shutdown_interface(self, interface: str):
        """Shutdown an interface."""
        if interface in self.interfaces:
            self.interfaces[interface]["status"] = "administratively down"
            self.interfaces[interface]["protocol"] = "down"

    def no_shutdown_interface(self, interface: str):
        """Bring up an interface."""
        if interface in self.interfaces:
            self.interfaces[interface]["status"] = "up"
            self.interfaces[interface]["protocol"] = "up"

    def save_config(self):
        """Copy running-config to startup-config."""
        self.startup_config = self.running_config.copy()
        return True

    def get_running_config(self) -> str:
        """Generate running configuration text."""
        config_lines = [
            "Building configuration...",
            "",
            "Current configuration : 1234 bytes",
            "!",
            f"version {self.ios_version}",
            "!",
            f"hostname {self.running_config['hostname']}",
            "!"
        ]

        if self.running_config.get("enable_secret"):
            config_lines.append(f"enable secret 5 {self.running_config['enable_secret']}")
        elif self.running_config.get("enable_password"):
            config_lines.append(f"enable password {self.running_config['enable_password']}")

        config_lines.append("!")

        # Interface configurations
        for iface_name, iface_config in self.running_config.get("interfaces", {}).items():
            config_lines.append(f"interface {iface_name}")
            if iface_config.get("description"):
                config_lines.append(f" description {iface_config['description']}")
            if iface_config.get("ip_address") and iface_config.get("subnet_mask"):
                config_lines.append(f" ip address {iface_config['ip_address']} {iface_config['subnet_mask']}")
            if iface_config.get("status") == "administratively down":
                config_lines.append(" shutdown")
            config_lines.append("!")

        config_lines.extend([
            "line con 0",
            "line vty 0 4",
            " login",
            "!",
            "end"
        ])

        return "\n".join(config_lines)

    def get_interface_status(self) -> List[tuple]:
        """Get status of all interfaces."""
        status_list = []
        for name, config in self.interfaces.items():
            status_list.append((
                name,
                config["ip_address"] or "unassigned",
                config["status"],
                config["protocol"]
            ))
        return status_list
