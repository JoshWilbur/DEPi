import redis
import requests
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)
devices = {}
stats_data = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/aggregator", methods=["GET"])
def aggregator():
    return render_template("aggregator.html", devices=devices, stats_data=stats_data)


@app.route("/update", methods=["GET", "POST"])
def update_readings():
    global devices
    global stats_data
    devices.clear()
    stats_data.clear()
    keys = cache.keys("*")

    for d in ["CPU", "GPU", "RAM"]:
        response = requests.get(f"http://stats:5252/device/{d}/get")
        if response.status_code == 200:
            stats_data[d] = response.json() # Had format response as JSON to get this working
        else:
            return f"Error getting stats! Data received: {stats_data}"

    for key in keys:
        data = cache.hgetall(key)
        temp = data.get("temperature")
        speed = data.get("speed")
        time = data.get("time")

        # Convert temperature to fahrenheit
        if temp:
            response = requests.post("http://unit:5252/convert_c2f", data={"temperature": temp})
            if response.status_code == 200:
                converted = response.text
            else:
                converted = "failed"
        
        # Convert raw time to something readable
        if time:
            response = requests.post("http://unit:5252/convert_time", data={"time": time})
            if response.status_code == 200:
                readable_time = response.text
            else:
                readable_time = "failed"

        devices[key] = {
            "temperature": data.get("temperature"),
            "conv_temp": converted,
            "load": data.get("load"),
            "speed": speed,
            "time": readable_time,
            "raw_time": time
        }
    
    # Sort by timestamp so new readings at top
    sorted_devices = sorted(devices.items(), key=lambda x: x[1]['raw_time'], reverse=True)
    devices = dict(sorted_devices)
    return redirect("/aggregator")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
