import redis
import time
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def index():
    return render_template("./input.html")


@app.route("/submit_data", methods=["POST"])
def submit_data():
    device = request.form["device"]
    temperature = request.form["temperature"]
    load = request.form["load"]

    # Load data into dictionary
    data = {
        "device": device,
        "temperature": temperature,
        "load": load,
        "time": time.time()
    }

    # Ensure temp and load data are numbers, then post
    if temperature.isnumeric() and load.isnumeric():
        cache.hset(device, mapping=data)
        return """
                <p>Data posted successfully</p>
                <a href="/aggregator"><button>Go to Aggregator</button></a>
                <a href="/input"><button>Back to Input</button></a>
                """
    else:
        return """
                <p>Error saving data! Ensure temperature and load are numbers</p>
                <a href="/input"><button>Back to Input</button></a>
                """


@app.route("/clear_data")
def clear_data():
    cache.flushdb()
    return """
            <p>Data cleared successfully</p>
            <a href="/input"><button>Back to Input</button></a>
             """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
