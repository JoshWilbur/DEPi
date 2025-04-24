import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


# Helper function for getting metric data for a device
def get_data(device, metric):
    keys = cache.keys(f"{device}@*")
    metric_data = []

    for key in keys:
        db_data = cache.hgetall(key)
        if metric in db_data:
            metric_data.append(float(db_data[metric]))
    
    return metric_data


@app.route("/")
def all_stats():
    return "This page will display recently calculated stats"


@app.route("/device/<device>/<metric>/min")
def minimum(device, metric):
    metric_data = get_data(device, metric)
    if not metric_data:
        return "No data found"
    minimum = min(metric_data)
    return f"{minimum}"


@app.route("/device/<device>/<metric>/max")
def maximum(device, metric):
    metric_data = get_data(device, metric)
    if not metric_data:
        return "No data found"
    maximum = max(metric_data)
    return f"{maximum}"


@app.route("/device/<device>/<metric>/mean")
def mean(device, metric):
    metric_data = get_data(device, metric)
    if not metric_data:
        return "No data found"
    mean = sum(metric_data) / len(metric_data)
    return f"{mean}"


@app.route("/device/<device>/<metric>/range")
def range(device, metric):
    min_stat = minimum(device, metric)
    max_stat = maximum(device, metric)
    range_stat = max_stat-min_stat
    return f"{range_stat}"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)