from flask import Flask, jsonify, render_template, request, redirect, session
from backend.data_api import get_latest_data

app = Flask(__name__)
app.secret_key = "vpp_secret_key"  # required for session

from datetime import datetime, timezone, timedelta
@app.template_filter('format_datetime')
def format_datetime(value):
    try:
        dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
    except ValueError:
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except:
            return str(value)
            
    ist = timezone(timedelta(hours=5, minutes=30))
    return dt.astimezone(ist).strftime('%Y-%m-%d %I:%M:%S %p') + " (IST)"



# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # TEMP LOGIN (upgrade later)
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# -------- LIVE DATA API --------
@app.route("/data")
def data():
    if "user" not in session:
        return jsonify({})
    return jsonify(get_latest_data())


# -------- BLOCKCHAIN EXPLORER DATA --------
@app.route("/blockchain")
def blockchain_view():
    if "user" not in session:
        return redirect("/")

    from backend.blockchain import Blockchain
    bc = Blockchain()
    bc.load()

    return jsonify(bc.chain)


# -------- BLOCKCHAIN EXPLORER PAGE --------
@app.route("/explorer")
def explorer_page():
    if "user" not in session:
        return redirect("/")

    from backend.blockchain import Blockchain
    bc = Blockchain()
    bc.load()

    # Reverse the chain so the newest blocks appear first
    blocks = bc.chain[::-1]
    return render_template("explorer.html", blocks=blocks)


# -------- CONSUMPTION METRICS --------
@app.route("/consumption")
def consumption():
    if "user" not in session:
        return redirect("/")
    return render_template("consumption.html")


# -------- PAYMENT HUB --------
@app.route("/payment")
def payment():
    if "user" not in session:
        return redirect("/")
    return render_template("payment.html")

# -------- FACTORY RESET --------
@app.route("/reset", methods=["POST"])
def reset_system():
    if "user" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    import json, os
    from backend.data_api import handler
    from backend.blockchain import Blockchain
    from datetime import datetime
    
    # 1. Zero out local accumulator matrices
    handler.ac_energy = 0.0
    handler.dc_energy = 0.0
    handler.uptime_minutes = 0.0
    handler.last_ts = None
    handler.last_ac_power = 0.0
    handler.last_dc_power = 0.0
    handler.last_ac_energy = 0.0
    handler.last_dc_energy = 0.0
    handler.batt_charge_wh = 0.0
    handler.batt_discharge_wh = 0.0
    
    # 2. Obliterate local blockchain array
    bc = Blockchain()
    bc.chain = []
    bc.prev_hash = "0"
    bc.save()
    
    # 3. Mark the explicit temporal point of destruction
    try:
        config_path = os.path.join(os.path.dirname(__file__), "backend", "reset_config.json")
        with open(config_path, "w") as f:
            json.dump({"reset_timestamp": datetime.utcnow().isoformat() + "Z"}, f)
    except Exception as e:
        print("Failed to write reset state:", e)
        
    return jsonify({"success": True})

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)