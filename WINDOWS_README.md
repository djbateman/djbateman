# Running on Windows

The Cisco Router Simulator now works on Windows! The `readline` module (used for command history and line editing) is optional.

## Quick Start

```powershell
python main.py
```

## Optional: Enhanced Command Line Experience

For command history and line editing features (arrow keys, command recall), install `pyreadline3`:

```powershell
pip install pyreadline3
```

**Note:** Without `pyreadline3`, the simulator works perfectly but you won't have:
- Up/Down arrow keys for command history
- Tab completion
- Line editing with Left/Right arrows

These features are nice-to-have but not required for full functionality.

## Testing

Run the quick test to verify everything works:

```powershell
python quick_test.py
```

## Common Issues

### ModuleNotFoundError: No module named 'readline'
**Solution:** This is fixed! The module is now optional. Just run the program normally.

### Commands not working after the first one
**Solution:** This is fixed! You can now run multiple commands in sequence.

## Example Usage

```
Router> enable
Router# configure terminal
Router(config)# hostname MyRouter
MyRouter(config)# interface GigabitEthernet0/0
MyRouter(config-if)# ip address 192.168.1.1 255.255.255.0
MyRouter(config-if)# no shutdown
MyRouter(config-if)# end
MyRouter# show ip interface brief
```
