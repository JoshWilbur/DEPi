import redis
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/convert_c2f", methods=["POST"])
def convert_c2f():
    temp = request.form.get("temperature")

    if not temp:
        return "Missing temperature data"
    
    celsius = float(temp)
    fahrenheit = (celsius * 1.8) + 32
    return f"{fahrenheit: .2f}"


@app.route("/convert_time", methods=["POST"])
def convert_time():
    raw_time = request.form.get("time")

    if not raw_time:
        return "Missing temperature data"
    
    formatted_time = datetime.fromtimestamp(float(raw_time)).strftime("%Y-%m-%d %H:%M:%S UTC")
    return formatted_time


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)