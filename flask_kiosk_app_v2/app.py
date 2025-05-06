from flask import Flask, render_template, request, redirect, url_for
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

app = Flask(__name__)

charges = {20: 2, 40: 4, 60: 6, 80: 8, 100: 10}
MAX_COINS = 1000
remaining_coins = MAX_COINS
last_amount = 0
log_file = "transactions.log"
log_tag = "kiosk"

# Setup file logger with rotation
logger = logging.getLogger("TransactionLogger")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_last_remaining_coins():
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "Remaining:" in line:
                    remaining = int(line.strip().split("Remaining: ")[-1])
                    return remaining
    except Exception as e:
        print(f"Error reading log: {e}")
    return MAX_COINS


def log_to_journal(message):
    try:
        subprocess.run(['logger', '-t', log_tag, message], check=True)
    except Exception as e:
        print(f"systemd journal logging failed: {e}")


@app.route("/")
def welcome():
    remaining = get_last_remaining_coins()
    if remaining <= 100:
        return render_template("no_coins.html")
    return render_template("welcome.html")


@app.route("/select")
def select():
    remaining = get_last_remaining_coins()
    if remaining <= 100:
        return render_template("no_coins.html")
    return render_template("select.html")


@app.route("/result", methods=["POST"])
def result():
    global last_amount
    if get_last_remaining_coins() <= 100:
        return render_template("no_coins.html")

    amount = int(request.form["amount"])
    last_amount = amount
    charge = charges.get(amount, 0)
    total = amount + charge

    return render_template("result.html", amount=amount, charge=charge, total=total)


@app.route("/qrcode", methods=["POST"])
def qrcode():
    global last_amount, remaining_coins

    remaining_coins = get_last_remaining_coins()
    if remaining_coins <= 100:
        return render_template("no_coins.html")

    amount = last_amount
    charge = charges.get(amount, 0)
    total = amount + charge

    remaining_coins -= amount
    log_message = f"Amount: {amount}, Charge: {charge}, Total: {total}, Remaining: {remaining_coins}"
    logger.info(log_message)
    log_to_journal(log_message)

    if remaining_coins <= 100:
        warning_msg = f"Low Coin Warning: Only {remaining_coins} coins left."
        logger.error(warning_msg)
        log_to_journal(warning_msg)

    qr_filename = f"qrcode_{amount}.png"
    return render_template("qrcode.html", qr_filename=qr_filename)


@app.route("/execute")
def execute_script():
    global last_amount
    script_path = f"./arduino_scripts/trigger_{last_amount}.sh"
    try:
        subprocess.Popen(["bash", script_path])
    except Exception as e:
        logger.error(f"Error executing script: {e}")
        log_to_journal(f"Script execution error: {e}")
    return redirect(url_for("welcome"))


@app.route("/abort")
def abort():
    return redirect(url_for("welcome"))


@app.route("/admin/reset")
def admin_reset():
    global remaining_coins
    remaining_coins = MAX_COINS
    msg = "ADMIN: Coin count reset to MAX."
    logger.info(msg)
    log_to_journal(msg)
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    app.run(debug=True)
