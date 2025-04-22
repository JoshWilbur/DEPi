import redis
from flask import Flask, render_template, redirect

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def home():
    return render_template("./home.html")


@app.route("/aggregator", methods=["GET"])
def aggregator():
    keys = cache.keys("*")
    devices = {}
    for key in keys:
        data = cache.hgetall(key)
        devices[key] = {
            "temperature": data.get("temperature"),
            "load": data.get("load"),
            "time": data.get("time")
        }
    return render_template("aggregator.html", devices=devices)


@app.route("/update", methods=["GET"])
def update_readings():
    return redirect("/aggregator")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
