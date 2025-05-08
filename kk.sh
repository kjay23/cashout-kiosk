#!/bin/bash

echo "🔍 Monitoring Android notifications from KDE Connect..."

dbus-monitor "interface='org.freedesktop.Notifications'" |
while read -r line; do
    if echo "$line" | grep -q "You have received PHP 1.00 of GCash from"; then
        echo "✅ Messenger notification detected!"
        konsole -e htop

    elif echo "$line" | grep -q "You have received PHP 2.00 of GCash from"; then
        echo "💸 Received 200 PHP notification detected!"
        dolphin &

    # 🔧 Add more blocks below for additional phrases or app notifications:
    # elif echo "$line" | grep -q "Another Keyword or Phrase"; then
    #     echo "Matched Another Condition!"
    #     some_command_here
    fi
done
