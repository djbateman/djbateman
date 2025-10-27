#!/bin/bash
# Test script to verify multiple commands work in the CLI

echo "Testing multiple commands in the CLI..."
echo ""

# Send multiple commands to the simulator
python3 main.py <<EOF
enable
show version
configure terminal
hostname TestRouter
exit
show running-config
exit
EOF

echo ""
echo "Test completed!"
