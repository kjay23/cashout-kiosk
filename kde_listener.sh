#!/bin/bash

echo "🔍 Monitoring Android notifications from KDE Connect..."

dbus-monitor "interface='org.freedesktop.Notifications'" |
while read -r line; do
    if echo "$line" | grep -q "You have received PHP 20.00 of GCash from"; then
        echo "20 peso coin is dispensing..."
        bash /path/to/trigger_20.sh
        curl http://localhost:5000/execute

    elif echo "$line" | grep -q "You have received PHP 40.00 of GCash from"; then
        echo "40 pesos coin is dispensing..."
        bash /path/to/trigger_40.sh
        curl http://localhost:5000/execute

    elif echo "$line" | grep -q "You have received PHP 60.00 of GCash from"; then
        echo "60 pesos coin is dispensing..."
        bash /path/to/trigger_60.sh
        curl http://localhost:5000/execute

    elif echo "$line" | grep -q "You have received PHP 80.00 of GCash from"; then
        echo "80 pesos coin is dispensing..."
        bash /path/to/trigger_80.sh
        curl http://localhost:5000/execute

    elif echo "$line" | grep -q "You have received PHP 100.00 of GCash from"; then
        echo "100 pesos coin is dispensing..."
        bash /path/to/trigger_100.sh
        curl http://localhost:5000/execute
    fi
done
