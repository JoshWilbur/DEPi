import redis
import time
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def index():
    return render_template("input.html")


@app.route("/submit_data", methods=["POST"])
def submit_data():
    device = request.form["device"]
    temperature = request.form["temperature"]
    load = request.form["load"]
    speed = request.form["speed"]
    timestamp = time.time()
    key = f"{device}@{int(timestamp)}" # Unique key

    # Load data into dictionary
    data = {
        "temperature": temperature,
        "load": load,
        "speed": speed,
        "time": timestamp
    }

    # Ensure temp and load data are numbers, then post
    if temperature.isnumeric() and load.isnumeric() and speed.isnumeric():
        cache.hset(key, mapping=data)
        return """
                <p>Data posted successfully</p>
                <a href="/aggregator"><button>Go to Aggregator</button></a>
                <a href="/input"><button>Back to Input</button></a>
                """
    else:
        return """
                <p>Error saving data! Ensure all inputs are integers</p>
                <a href="/input"><button>Back to Input</button></a>
                """


@app.route("/clear_data")
def clear_data():
    cache.flushall()
    return """
            <p>Data cleared successfully</p>
            <a href="/input"><button>Back to Input</button></a>
             """

@app.route("/debug")
def debug():
    keys = cache.keys("*")
    return f"{keys}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
