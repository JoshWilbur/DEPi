import redis
import time
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def index():
    return "Welcome to the data entry service! Please go to /submit_data"


@app.route("/submit_data", methods=["GET", "POST"])
def data_entry():
    if request.method == "POST":
        device = request.form.get("device")
        temperature = request.form.get("temperature")
        load = request.form.get("load")

        # Ensure temp and load data are numbers, then post
        if temperature.isnumeric() and load.isnumeric():
            cache.hset(f"device:{device}", mapping={
                "temperature": temperature,
                "load": load,
                "time": time.time()
            })
            return f"{device} data posted successfully"
        else:
            return "Error saving data"

    return render_template("./input.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
