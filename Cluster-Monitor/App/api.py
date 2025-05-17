from flask import Flask, jsonify, render_template
from App.monitor import get_all_metrics

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return jsonify(get_all_metrics())

@app.route("/")
def dashboard():
    return render_template("index.html")
