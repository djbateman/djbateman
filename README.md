# Cisco Router Simulator

A Python-based Cisco IOS router simulator that provides an interactive command-line interface (CLI) mimicking Cisco router behavior. Perfect for learning Cisco commands, testing network configurations, or practicing for CCNA certification without physical hardware.

## Features

- **Authentic Cisco IOS CLI Experience**: Mimics the look and feel of real Cisco IOS
- **Multiple CLI Modes**: User EXEC, Privileged EXEC, Global Configuration, and Interface Configuration modes
- **Interface Management**: Configure GigabitEthernet and Serial interfaces
- **IP Address Configuration**: Assign IP addresses and subnet masks to interfaces
- **Running and Startup Configuration**: Save and view configurations
- **Common Show Commands**: `show version`, `show running-config`, `show ip interface brief`, etc.
- **Interface Status Control**: Enable/disable interfaces with `shutdown` and `no shutdown`
- **Command History**: Navigate through previously entered commands

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd djbateman
```

2. No external dependencies required - uses only Python standard library!

## Usage

### Starting the Simulator

```bash
python main.py
```

Or with a custom hostname:

```bash
python main.py --hostname R1
```

### Basic Command Examples

#### 1. Enter Privileged Mode
```
Router> enable
Router#
```

#### 2. View System Information
```
Router# show version
```

#### 3. Enter Configuration Mode
```
Router# configure terminal
Enter configuration commands, one per line. End with CNTL/Z.
Router(config)#
```

#### 4. Change Hostname
```
Router(config)# hostname R1
R1(config)#
```

#### 5. Configure an Interface
```
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# description LAN Interface
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)#
```

#### 6. View Interface Status
```
R1# show ip interface brief
```

#### 7. View Running Configuration
```
R1# show running-config
```

#### 8. Save Configuration
```
R1# write
Building configuration...
[OK]
```

Or:
```
R1# copy running-config startup-config
```

## Supported Commands

### User EXEC Mode (>)
- `enable` - Enter privileged EXEC mode
- `show version` - Display system version information
- `show ip interface brief` - Display brief interface status
- `ping <ip>` - Send ICMP echo requests
- `exit` - Exit the CLI
- `?` - Display help

### Privileged EXEC Mode (#)
- `configure terminal` - Enter global configuration mode
- `show running-config` - Display current configuration
- `show startup-config` - Display saved configuration
- `show interfaces [interface]` - Display detailed interface information
- `show ip route` - Display routing table
- `show ip interface brief` - Display brief interface status
- `write` - Save running configuration to startup configuration
- `copy running-config startup-config` - Save configuration
- `disable` - Return to user EXEC mode
- `reload` - Restart the router
- `exit` - Exit the CLI

### Global Configuration Mode (config)#
- `hostname <name>` - Set router hostname
- `enable password <password>` - Set enable password
- `enable secret <password>` - Set encrypted enable password
- `interface <interface>` - Enter interface configuration mode
- `exit` - Return to privileged EXEC mode
- `end` - Return to privileged EXEC mode

### Interface Configuration Mode (config-if)#
- `ip address <ip> <mask>` - Set IP address and subnet mask
- `description <text>` - Set interface description
- `shutdown` - Administratively disable the interface
- `no shutdown` - Enable the interface
- `exit` - Return to global configuration mode
- `end` - Return to privileged EXEC mode

## Available Interfaces

The simulator includes the following interfaces:

- **GigabitEthernet0/0** (can be abbreviated as `gi0/0`)
- **GigabitEthernet0/1** (can be abbreviated as `gi0/1`)
- **Serial0/0/0** (can be abbreviated as `se0/0/0`)

## Architecture

The simulator consists of four main components:

### 1. `cisco_router.py`
Core router class that manages:
- Router state and configuration
- Interface management
- Configuration storage (running-config and startup-config)
- System information

### 2. `cli_interface.py`
Command-line interface implementation:
- Mode management (User EXEC, Privileged EXEC, Config modes)
- Command parsing and routing
- Prompt generation
- User interaction handling

### 3. `commands.py`
Command handlers for:
- Show commands (version, config, interfaces, routes)
- Configuration display
- System information formatting

### 4. `main.py`
Application entry point:
- Command-line argument parsing
- Router initialization
- CLI startup

## Example Session

```
============================================================
  Cisco Router Simulator
  Simulating Cisco IOS
============================================================

Router> enable
Router# configure terminal
Enter configuration commands, one per line. End with CNTL/Z.
Router(config)# hostname CoreRouter
CoreRouter(config)# interface GigabitEthernet0/0
CoreRouter(config-if)# ip address 10.0.1.1 255.255.255.0
CoreRouter(config-if)# description Core Network Interface
CoreRouter(config-if)# no shutdown
CoreRouter(config-if)# exit
CoreRouter(config)# interface GigabitEthernet0/1
CoreRouter(config-if)# ip address 10.0.2.1 255.255.255.0
CoreRouter(config-if)# no shutdown
CoreRouter(config-if)# end
CoreRouter# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.1.1        YES manual  up                    up
GigabitEthernet0/1     10.0.2.1        YES manual  up                    up
Serial0/0/0            unassigned      YES manual  administratively down down
CoreRouter# write
Building configuration...
[OK]
CoreRouter#
```

## Educational Use

This simulator is ideal for:

- **Learning Cisco IOS commands** without needing physical routers
- **CCNA exam preparation** - practice configuration tasks
- **Network automation testing** - test scripts before deploying to real hardware
- **Teaching basic networking concepts** in a classroom environment
- **Prototyping configurations** before implementing on production equipment

## Limitations

This is a simulator for educational purposes. It does NOT:

- Actually route network traffic
- Implement real networking protocols (OSPF, EIGRP, BGP, etc.)
- Support all Cisco IOS commands
- Provide actual network connectivity
- Implement security features like AAA or encryption
- Support all interface types or modules

## Contributing

Contributions are welcome! Some ideas for enhancements:

- Add support for VLANs
- Implement static routing
- Add ACL (Access Control List) support
- Support for additional show commands
- DHCP server configuration
- NAT configuration
- More realistic command validation
- Tab completion for commands

## License

This project is open source and available for educational purposes.

## Acknowledgments

Inspired by Cisco IOS and created as a learning tool for network engineers and students.

---

**Note**: This is a simulator for educational purposes only. It does not replace hands-on experience with real Cisco equipment or official Cisco training materials.
