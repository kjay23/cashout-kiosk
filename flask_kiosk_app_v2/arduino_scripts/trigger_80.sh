#!/bin/bash

INO_NAME="CoinDispenser4"
INO_FILE="/tmp/CoinDispenser4/CoinDispenser4.ino"
TMP_DIR="/tmp/CoinDispenser4"
BOARD="arduino:avr:uno"

# Determine available serial port
if [ -e /dev/ttyACM0 ]; then
    PORT="/dev/ttyACM0"
else
    PORT="/dev/ttyUSB0"
fi

echo "Using port: $PORT"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
cp "./arduino_scripts/CoinDispenser4.ino" "$INO_FILE"

arduino-cli compile --fqbn "$BOARD" "$TMP_DIR"
arduino-cli upload -p "$PORT" --fqbn "$BOARD" "$TMP_DIR"

if [ $? -eq 0 ]; then
    echo "Upload successful!"
else
    echo "Upload failed!"
fi
