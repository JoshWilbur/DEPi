import redis
import requests
from flask import Flask, render_template, redirect

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)
devices = {}


@app.route("/")
def home():
    return render_template("./home.html")


@app.route("/aggregator", methods=["GET"])
def aggregator():
    return render_template("aggregator.html", devices=devices)


@app.route("/update", methods=["GET"])
def update_readings():
    keys = cache.keys("*")
    for key in keys:
        data = cache.hgetall(key)
        temp = data.get("temperature")
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
            "time": readable_time
        }
    
    return redirect("/aggregator")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
