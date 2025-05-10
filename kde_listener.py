import subprocess
import re
import os

# Mapping of amount strings to corresponding script paths
AMOUNT_SCRIPTS = {
    "20": "/path/to/trigger_20.sh",
    "40": "/path/to/trigger_40.sh",
    "60": "/path/to/trigger_60.sh",
    "80": "/path/to/trigger_80.sh",
    "100": "/path/to/trigger_100.sh",
}

def execute_script(amount):
    script_path = AMOUNT_SCRIPTS.get(amount)
    if script_path and os.path.isfile(script_path):
        print(f"Executing script for {amount} pesos: {script_path}")
        subprocess.run(["bash", script_path])
    else:
        print(f"Script not found for amount: {amount} (Expected at {script_path})")

def monitor_notifications():
    print("🔍 Monitoring Android notifications from KDE Connect...")

    # Start dbus-monitor process
    process = subprocess.Popen(
        ["dbus-monitor", "interface='org.freedesktop.Notifications'"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        if "string" in line and "received" in line.lower():
            print("Notification line:", line.strip())

            for amount in AMOUNT_SCRIPTS.keys():
                # Match whole amount word, e.g., '60', '60.00', etc.
                if re.search(rf"\b{amount}(\.00)?\b", line):
                    execute_script(amount)
                    break

if __name__ == "__main__":
    try:
        monitor_notifications()
    except KeyboardInterrupt:
        print("\nStopped listening.")
