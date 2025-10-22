"""
Cisco Router Simulator - CLI Interface
Implements the command-line interface with IOS-like behavior.
"""

import readline
import shlex
from typing import Optional, List, Tuple
from commands import CommandHandler


class Mode:
    """CLI Mode constants."""
    USER_EXEC = "user"
    PRIVILEGED_EXEC = "privileged"
    GLOBAL_CONFIG = "global_config"
    INTERFACE_CONFIG = "interface_config"


class CLIInterface:
    """Command Line Interface for the Cisco router simulator."""

    def __init__(self, router):
        self.router = router
        self.command_handler = CommandHandler(router)
        self.mode = Mode.USER_EXEC
        self.current_interface = None
        self.running = True
        self.command_history = []

    def get_prompt(self) -> str:
        """Return the appropriate prompt based on current mode."""
        hostname = self.router.hostname

        if self.mode == Mode.USER_EXEC:
            return f"{hostname}>"
        elif self.mode == Mode.PRIVILEGED_EXEC:
            return f"{hostname}#"
        elif self.mode == Mode.GLOBAL_CONFIG:
            return f"{hostname}(config)#"
        elif self.mode == Mode.INTERFACE_CONFIG:
            return f"{hostname}(config-if)#"

        return f"{hostname}>"

    def print_banner(self):
        """Display login banner."""
        print("\n" + "=" * 60)
        print("  Cisco Router Simulator")
        print("  Simulating Cisco IOS")
        print("=" * 60 + "\n")

    def parse_command(self, command_line: str) -> Tuple[str, List[str]]:
        """Parse command line into command and arguments."""
        try:
            parts = shlex.split(command_line)
            if not parts:
                return "", []
            return parts[0], parts[1:]
        except ValueError:
            return command_line.split()[0] if command_line.split() else "", []

    def execute_command(self, command_line: str) -> Optional[str]:
        """Execute a command and return output."""
        command_line = command_line.strip()

        if not command_line:
            return None

        # Store in history
        self.command_history.append(command_line)

        # Parse command
        parts = command_line.split()
        cmd = parts[0].lower()

        try:
            # Common commands across all modes
            if cmd == "exit" or cmd == "quit":
                return self.handle_exit()
            elif cmd == "?":
                return self.handle_help()
            elif cmd == "end":
                if self.mode in [Mode.GLOBAL_CONFIG, Mode.INTERFACE_CONFIG]:
                    self.mode = Mode.PRIVILEGED_EXEC
                    return None
                return "% Invalid input detected at '^' marker."

            # User EXEC mode commands
            if self.mode == Mode.USER_EXEC:
                return self.handle_user_exec(parts)

            # Privileged EXEC mode commands
            elif self.mode == Mode.PRIVILEGED_EXEC:
                return self.handle_privileged_exec(parts)

            # Global configuration mode commands
            elif self.mode == Mode.GLOBAL_CONFIG:
                return self.handle_global_config(parts)

            # Interface configuration mode commands
            elif self.mode == Mode.INTERFACE_CONFIG:
                return self.handle_interface_config(parts)

        except Exception as e:
            return f"% Error: {str(e)}"

        return None

    def handle_user_exec(self, parts: List[str]) -> Optional[str]:
        """Handle commands in user EXEC mode."""
        cmd = parts[0].lower()

        if cmd == "enable":
            # In a real router, this would ask for password
            # For simplicity, we'll just switch modes
            if len(parts) > 1:
                password = parts[1]
                if self.router.verify_enable_password(password):
                    self.mode = Mode.PRIVILEGED_EXEC
                    return None
                else:
                    return "% Bad secrets"
            else:
                # Simplified: just allow enable without password for demo
                self.mode = Mode.PRIVILEGED_EXEC
                return None

        elif cmd == "show":
            return self.handle_show_command(parts[1:])

        elif cmd == "ping":
            if len(parts) < 2:
                return "% Incomplete command."
            return self.command_handler.ping(parts[1])

        else:
            return f"% Invalid input detected at '{cmd}' marker."

    def handle_privileged_exec(self, parts: List[str]) -> Optional[str]:
        """Handle commands in privileged EXEC mode."""
        cmd = parts[0].lower()

        if cmd == "disable":
            self.mode = Mode.USER_EXEC
            return None

        elif cmd == "configure":
            if len(parts) > 1 and parts[1].lower() == "terminal":
                self.mode = Mode.GLOBAL_CONFIG
                return "Enter configuration commands, one per line. End with CNTL/Z."
            return "% Incomplete command."

        elif cmd == "show":
            return self.handle_show_command(parts[1:])

        elif cmd == "write" or (cmd == "copy" and len(parts) > 2 and
                                 parts[1] == "running-config" and parts[2] == "startup-config"):
            if self.router.save_config():
                return "Building configuration...\n[OK]"
            return "% Failed to save configuration"

        elif cmd == "reload":
            return "Proceed with reload? [confirm]"

        elif cmd == "ping":
            if len(parts) < 2:
                return "% Incomplete command."
            return self.command_handler.ping(parts[1])

        else:
            return f"% Invalid input detected at '{cmd}' marker."

    def handle_global_config(self, parts: List[str]) -> Optional[str]:
        """Handle commands in global configuration mode."""
        cmd = parts[0].lower()

        if cmd == "hostname":
            if len(parts) < 2:
                return "% Incomplete command."
            self.router.set_hostname(parts[1])
            return None

        elif cmd == "enable":
            if len(parts) < 2:
                return "% Incomplete command."

            if parts[1].lower() == "password":
                if len(parts) < 3:
                    return "% Incomplete command."
                self.router.set_enable_password(parts[2], secret=False)
                return None

            elif parts[1].lower() == "secret":
                if len(parts) < 3:
                    return "% Incomplete command."
                self.router.set_enable_password(parts[2], secret=True)
                return None

        elif cmd == "interface":
            if len(parts) < 2:
                return "% Incomplete command."

            interface_name = parts[1]
            # Normalize interface name
            interface_name = self.normalize_interface_name(interface_name)

            if interface_name in self.router.interfaces:
                self.mode = Mode.INTERFACE_CONFIG
                self.current_interface = interface_name
                return None
            else:
                return f"% Invalid interface type and number"

        elif cmd == "no":
            # Handle 'no' commands
            if len(parts) < 2:
                return "% Incomplete command."
            return f"Removed configuration for {' '.join(parts[1:])}"

        else:
            return f"% Invalid input detected at '{cmd}' marker."

    def handle_interface_config(self, parts: List[str]) -> Optional[str]:
        """Handle commands in interface configuration mode."""
        cmd = parts[0].lower()

        if cmd == "ip":
            if len(parts) < 2:
                return "% Incomplete command."

            if parts[1].lower() == "address":
                if len(parts) < 4:
                    return "% Incomplete command."

                ip_address = parts[2]
                subnet_mask = parts[3]

                self.router.configure_interface(
                    self.current_interface,
                    ip_address=ip_address,
                    subnet_mask=subnet_mask
                )
                return None

        elif cmd == "description":
            if len(parts) < 2:
                return "% Incomplete command."

            description = " ".join(parts[1:])
            self.router.configure_interface(
                self.current_interface,
                description=description
            )
            return None

        elif cmd == "shutdown":
            self.router.shutdown_interface(self.current_interface)
            return None

        elif cmd == "no":
            if len(parts) >= 2 and parts[1].lower() == "shutdown":
                self.router.no_shutdown_interface(self.current_interface)
                return None
            return "% Incomplete command."

        else:
            return f"% Invalid input detected at '{cmd}' marker."

    def handle_show_command(self, args: List[str]) -> Optional[str]:
        """Handle 'show' commands."""
        if not args:
            return "% Incomplete command."

        subcmd = args[0].lower()

        if subcmd == "version":
            return self.command_handler.show_version()

        elif subcmd == "running-config":
            if self.mode == Mode.USER_EXEC:
                return "% Invalid input detected at '^' marker."
            return self.command_handler.show_running_config()

        elif subcmd == "startup-config":
            if self.mode == Mode.USER_EXEC:
                return "% Invalid input detected at '^' marker."
            return self.command_handler.show_startup_config()

        elif subcmd == "ip":
            if len(args) < 2:
                return "% Incomplete command."

            if args[1].lower() == "interface":
                if len(args) > 2 and args[2].lower() == "brief":
                    return self.command_handler.show_ip_interface_brief()
                return "% Incomplete command."

            elif args[1].lower() == "route":
                return self.command_handler.show_ip_route()

        elif subcmd == "interfaces":
            if len(args) > 1:
                interface = self.normalize_interface_name(args[1])
                return self.command_handler.show_interfaces(interface)
            return self.command_handler.show_interfaces()

        elif subcmd == "interface":
            if len(args) > 1:
                interface = self.normalize_interface_name(args[1])
                return self.command_handler.show_interfaces(interface)
            return "% Incomplete command."

        return f"% Invalid input detected at '{subcmd}' marker."

    def handle_exit(self) -> Optional[str]:
        """Handle exit command."""
        if self.mode == Mode.INTERFACE_CONFIG:
            self.mode = Mode.GLOBAL_CONFIG
            self.current_interface = None
        elif self.mode == Mode.GLOBAL_CONFIG:
            self.mode = Mode.PRIVILEGED_EXEC
        elif self.mode == Mode.PRIVILEGED_EXEC:
            self.mode = Mode.USER_EXEC
        elif self.mode == Mode.USER_EXEC:
            self.running = False
            return "Goodbye!"
        return None

    def handle_help(self) -> str:
        """Display help based on current mode."""
        if self.mode == Mode.USER_EXEC:
            return """Available commands:
  enable              Enter privileged EXEC mode
  show                Show running system information
  ping                Send echo messages
  exit                Exit from the EXEC
  ?                   Display this help"""

        elif self.mode == Mode.PRIVILEGED_EXEC:
            return """Available commands:
  configure terminal  Enter global configuration mode
  show                Show running system information
  write               Write running configuration to memory
  copy running-config startup-config
  disable             Exit privileged EXEC mode
  reload              Halt and perform a cold restart
  ping                Send echo messages
  exit                Exit from the EXEC
  ?                   Display this help"""

        elif self.mode == Mode.GLOBAL_CONFIG:
            return """Available commands:
  hostname            Set system's network name
  interface           Select an interface to configure
  enable password     Set enable password
  enable secret       Set enable secret
  no                  Negate a command or set its defaults
  exit                Exit from configuration mode
  end                 Exit to privileged EXEC mode
  ?                   Display this help"""

        elif self.mode == Mode.INTERFACE_CONFIG:
            return """Available commands:
  ip address          Set the IP address of an interface
  description         Interface specific description
  shutdown            Shutdown the selected interface
  no shutdown         Enable the selected interface
  exit                Exit from interface configuration mode
  end                 Exit to privileged EXEC mode
  ?                   Display this help"""

        return "Help not available for current mode."

    def normalize_interface_name(self, name: str) -> str:
        """Normalize interface names (e.g., gi0/0 -> GigabitEthernet0/0)."""
        name = name.lower()

        # Common abbreviations
        if name.startswith("gi") or name.startswith("gig"):
            return "GigabitEthernet" + name[name.find("0"):]
        elif name.startswith("fa") or name.startswith("fast"):
            return "FastEthernet" + name[name.find("0"):]
        elif name.startswith("se") or name.startswith("serial"):
            return "Serial" + name[name.find("0"):]
        elif name.startswith("e") or name.startswith("eth"):
            return "Ethernet" + name[name.find("0"):]

        # Return as-is if already in full form
        for iface in self.router.interfaces.keys():
            if name.lower() == iface.lower():
                return iface

        return name

    def run(self):
        """Main CLI loop."""
        self.print_banner()

        while self.running:
            try:
                prompt = self.get_prompt()
                user_input = input(f"{prompt} ")

                output = self.execute_command(user_input)
                if output:
                    print(output)

            except KeyboardInterrupt:
                print("\n")
                continue
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"% Error: {str(e)}")
