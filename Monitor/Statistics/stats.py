import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def all_stats():
    return "This page will display recently calculated stats"


@app.route("/device/<device>/min")
def minimum():
    return "This endpoint will calculate the minimum value for a data set on a device"


@app.route("/device/<device>/max")
def maximum():
    return "This endpoint will calculate the maximum value for a data set on a device"


@app.route("/device/<device>/mean")
def mean():
    return "This endpoint will calculate the mean value for a data set on a device"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)