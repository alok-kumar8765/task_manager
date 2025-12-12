# ==============================================================
#      FLASK + SOCKET.IO  REAL-TIME TASK MANAGER DASHBOARD V2
# ==============================================================

from flask import Flask, render_template, request, redirect, session, jsonify
from flask_socketio import SocketIO, emit
import psutil
import subprocess
import time
import threading

app = Flask(__name__)
app.secret_key = "super-secret-key"  # change in production
socketio = SocketIO(app, cors_allowed_origins="*")


# -------------------------------------------------------------
# SYSTEM DATA FUNCTIONS
# -------------------------------------------------------------
def get_system_data():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    net = psutil.net_io_counters()

    # GPU
    try:
        gpu = subprocess.getoutput(
            "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits"
        ).strip()
        gpu_usage = gpu + "%"
    except:
        gpu_usage = "N/A"

    # TOP PROCESSES
    processes = sorted(
        psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]),
        key=lambda p: p.info["cpu_percent"],
        reverse=True,
    )
    top = [
        {
            "pid": p.info["pid"],
            "name": p.info["name"],
            "cpu": p.info["cpu_percent"],
            "mem": p.info["memory_percent"],
        }
        for p in processes[:10]
    ]

    # SYSTEM LOG (simplified)
    logs = [
        f"CPU: {cpu}%",
        f"Memory: {mem}%",
        f"Disk: {disk}%",
        f"Bytes Sent: {net.bytes_sent}",
        f"Bytes Received: {net.bytes_recv}",
    ]

    return {
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "gpu": gpu_usage,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
        "processes": top,
        "logs": logs,
        "timestamp": time.time(),
    }


# -------------------------------------------------------------
# BACKGROUND THREAD: EMIT REAL-TIME DATA
# -------------------------------------------------------------
def background_task():
    while True:
        socketio.emit("update", get_system_data())
        socketio.sleep(1)


threading.Thread(target=background_task, daemon=True).start()


# -------------------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["user"] = "admin"
            return redirect("/dashboard")
        return "Invalid credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------------------------------------------------
# API (theme toggle)
# -------------------------------------------------------------
@app.route("/api/theme", methods=["POST"])
def api_theme():
    session["theme"] = request.json["theme"]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
