"""
Cisco Router Simulator - Command Handlers
Implements handlers for various Cisco IOS commands.
"""

from typing import Optional, List


class CommandHandler:
    """Handles execution of Cisco IOS commands."""

    def __init__(self, router):
        self.router = router

    def show_version(self) -> str:
        """Display IOS version and system information."""
        uptime = self.router.get_uptime()
        return f"""Cisco IOS Software, C2900 Software (C2900-UNIVERSALK9-M), Version {self.router.ios_version}, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Wed 11-Feb-15 15:18 by prod_rel_team

ROM: System Bootstrap, Version 15.0(1r)M16, RELEASE SOFTWARE (fc1)

{self.router.hostname} uptime is {uptime}
System returned to ROM by power-on
System image file is "flash:c2900-universalk9-mz.SPA.151-4.M10.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

Cisco {self.router.model} (revision 1.0) with 491520K/32768K bytes of memory.
Processor board ID FTX1628835J
3 Gigabit Ethernet interfaces
1 Serial(sync/async) interface
DRAM configuration is 64 bits wide with parity disabled.
255K bytes of non-volatile configuration memory.
250880K bytes of ATA System CompactFlash 0 (Read/Write)


License Info:

License UDI:

-------------------------------------------------
Device#   PID                   SN
-------------------------------------------------
*0        {self.router.model}          FTX1628835J



Technology Package License Information for Module:'c2900'

-----------------------------------------------------------------
Technology    Technology-package           Technology-package
              Current       Type           Next reboot
------------------------------------------------------------------
ipbase        ipbasek9      Permanent      ipbasek9
security      None          None           None
uc            None          None           None
data          None          None           None

Configuration register is 0x2102"""

    def show_running_config(self) -> str:
        """Display running configuration."""
        return self.router.get_running_config()

    def show_startup_config(self) -> str:
        """Display startup configuration."""
        if not self.router.startup_config:
            return "startup-config is not present"
        # For now, show similar to running config
        return "Startup configuration:\n" + self.router.get_running_config()

    def show_ip_interface_brief(self) -> str:
        """Display brief interface status."""
        lines = [
            "Interface              IP-Address      OK? Method Status                Protocol",
        ]

        for iface_name, iface_config in self.router.interfaces.items():
            ip_addr = iface_config.get("ip_address") or "unassigned"
            status = iface_config.get("status", "down")
            protocol = iface_config.get("protocol", "down")

            # Format: Interface name (23 chars), IP (16 chars), OK? (4), Method (7), Status (22), Protocol
            line = f"{iface_name:<23}{ip_addr:<16}YES manual  {status:<22}{protocol}"
            lines.append(line)

        return "\n".join(lines)

    def show_interfaces(self, interface: Optional[str] = None) -> str:
        """Display detailed interface information."""
        lines = []

        interfaces_to_show = [interface] if interface else self.router.interfaces.keys()

        for iface_name in interfaces_to_show:
            if iface_name not in self.router.interfaces:
                return "              ^\n% Invalid input detected at '^' marker."

            iface = self.router.interfaces[iface_name]
            lines.append(f"{iface_name} is {iface['status']}, line protocol is {iface['protocol']}")

            if iface.get('description'):
                lines.append(f"  Description: {iface['description']}")

            if 'mac_address' in iface:
                lines.append(f"  Hardware is {iface_name.split('/')[0]}, address is {iface['mac_address']} (bia {iface['mac_address']})")

            if iface.get('ip_address'):
                lines.append(f"  Internet address is {iface['ip_address']}/{iface.get('subnet_mask', '255.255.255.0')}")

            lines.append(f"  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,")
            lines.append(f"     reliability 255/255, txload 1/255, rxload 1/255")
            lines.append(f"  Encapsulation ARPA, loopback not set")
            lines.append(f"  Last input never, output never, output hang never")
            lines.append(f"  Last clearing of \"show interface\" counters never")
            lines.append(f"  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0")
            lines.append(f"  Queueing strategy: fifo")
            lines.append(f"  Output queue: 0/40 (size/max)")
            lines.append(f"  5 minute input rate 0 bits/sec, 0 packets/sec")
            lines.append(f"  5 minute output rate 0 bits/sec, 0 packets/sec")
            lines.append(f"     0 packets input, 0 bytes, 0 no buffer")
            lines.append(f"     Received 0 broadcasts (0 IP multicasts)")
            lines.append(f"     0 runts, 0 giants, 0 throttles")
            lines.append(f"     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored")
            lines.append(f"     0 watchdog, 0 multicast, 0 pause input")
            lines.append(f"     0 packets output, 0 bytes, 0 underruns")
            lines.append(f"     0 output errors, 0 collisions, 0 interface resets")
            lines.append(f"     0 unknown protocol drops")
            lines.append(f"     0 babbles, 0 late collision, 0 deferred")
            lines.append(f"     0 lost carrier, 0 no carrier, 0 pause output")
            lines.append(f"     0 output buffer failures, 0 output buffers swapped out")
            lines.append("")

        return "\n".join(lines)

    def show_ip_route(self) -> str:
        """Display IP routing table."""
        lines = [
            "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP",
            "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area",
            "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2",
            "       E1 - OSPF external type 1, E2 - OSPF external type 2",
            "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2",
            "       ia - IS-IS inter area, * - candidate default, U - per-user static route",
            "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP",
            "       + - replicated route, % - next hop override",
            "",
            "Gateway of last resort is not set",
            ""
        ]

        # Add connected routes from configured interfaces
        for iface_name, iface_config in self.router.interfaces.items():
            if iface_config.get('ip_address') and iface_config.get('status') == 'up':
                ip = iface_config['ip_address']
                lines.append(f"C    {ip}/24 is directly connected, {iface_name}")
                lines.append(f"L    {ip}/32 is directly connected, {iface_name}")

        if len(lines) == 11:  # Only headers, no routes
            return "% Network not in table"

        return "\n".join(lines)

    def ping(self, destination: str) -> str:
        """Simulate ping command."""
        return f"""Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to {destination}, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)"""

    def configure_hostname(self, hostname: str):
        """Configure router hostname."""
        self.router.set_hostname(hostname)
        return f"Hostname set to {hostname}"

    def configure_interface_ip(self, interface: str, ip_address: str, subnet_mask: str):
        """Configure IP address on interface."""
        if interface not in self.router.interfaces:
            raise ValueError(f"Interface {interface} does not exist")

        self.router.configure_interface(
            interface,
            ip_address=ip_address,
            subnet_mask=subnet_mask
        )
        return f"IP address {ip_address} {subnet_mask} configured on {interface}"

    def configure_interface_description(self, interface: str, description: str):
        """Configure interface description."""
        if interface not in self.router.interfaces:
            raise ValueError(f"Interface {interface} does not exist")

        self.router.configure_interface(interface, description=description)
        return f"Description set on {interface}"
