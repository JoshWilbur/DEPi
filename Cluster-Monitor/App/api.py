import psutil
from flask import Flask, jsonify, render_template
from App.monitor import get_all_metrics

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return jsonify(get_all_metrics())

@app.route('/api/self')
def self_stats():
    process = psutil.Process()
    cpu = process.cpu_percent(interval=0.1)
    mem = process.memory_info().rss / (1024 ** 2)  # in MB
    return jsonify({"cpu": cpu, "memory": mem})

@app.route("/")
def dashboard():
    return render_template("index.html")
