#!/bin/bash
# Interactive test script to demonstrate command abbreviations

echo "Testing command abbreviations in interactive mode..."
echo ""

python3 main.py <<EOF
en
sh ver
conf t
hostname ShortcutRouter
int gi0/0
desc Connected to LAN
no shut
exit
exit
sh run
sh ip int br
wr
exit
EOF

echo ""
echo "All shortcuts tested successfully!"
