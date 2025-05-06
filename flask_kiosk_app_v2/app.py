from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

charges = {20: 2, 40: 4, 60: 6, 80: 8, 100: 10}
last_amount = 0

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/select")
def select():
    return render_template("select.html")

@app.route("/result", methods=["POST"])
def result():
    global last_amount
    amount = int(request.form["amount"])
    last_amount = amount
    charge = charges.get(amount, 0)
    total = amount + charge
    return render_template("result.html", amount=amount, charge=charge, total=total)

@app.route("/qrcode", methods=["POST"])
def qrcode():
    global last_amount
    qr_filename = f"qrcode_{last_amount}.png"
    return render_template("qrcode.html", qr_filename=qr_filename)


@app.route("/execute")
def execute_script():
    global last_amount
    script_path = f"./arduino_scripts/trigger_{last_amount}.sh"
    try:
        subprocess.Popen(["bash", script_path])
    except Exception as e:
        print(f"Error executing script: {e}")
    return redirect(url_for("welcome"))

@app.route("/abort")
def abort():
    return redirect(url_for("welcome"))

if __name__ == "__main__":
    app.run(debug=True)
