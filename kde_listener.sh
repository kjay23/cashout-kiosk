#!/bin/bash

echo "🔍 Monitoring Android notifications from KDE Connect..."

dbus-monitor "interface='org.freedesktop.Notifications'" |
while read -r line; do
    if echo "$line" | grep -q "You have received PHP 22.00 of GCash from"; then
        echo "20 peso coin is dispensing..."
        curl "http://localhost:5000/execute?amount=20"

    elif echo "$line" | grep -q "You have received PHP 42.00 of GCash from"; then
        echo "40 pesos coin is dispensing..."
        curl "http://localhost:5000/execute?amount=40"

    elif echo "$line" | grep -q "You have received PHP 63.00 of GCash from"; then
        echo "60 pesos coin is dispensing..."
        curl "http://localhost:5000/execute?amount=60"

    elif echo "$line" | grep -q "You have received PHP 84.00 of GCash from"; then
        echo "80 pesos coin is dispensing..."
        curl "http://localhost:5000/execute?amount=80"

    elif echo "$line" | grep -q "You have received PHP 105.00 of GCash from"; then
        echo "100 pesos coin is dispensing..."
        curl "http://localhost:5000/execute?amount=100"
    fi
done
