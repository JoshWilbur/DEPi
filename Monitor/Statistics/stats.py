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
    return """
        <p>These buttons direct you to each device's statistics</p><br>
        <a href="/stats/device/cpu"><button>CPU Statistics</button></a>
        <a href="/stats/device/gpu"><button>GPU Statistics</button></a>
        <a href="/stats/device/ram"><button>RAM Statistics</button></a>
        <a href="/"><button>Back</button></a>
    """


@app.route("/device/<device>")
def device_stats(device):
    temp_data = get_data(device, temperature)
    load_data = get_data(device, load)
    speed_data = get_data(device, speed) # TODO: finish
    return "This page will show all stats for a given device"


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
def range_stat(device, metric):
    metric_data = get_data(device, metric)
    if not metric_data:
        return "No data found"
    min_val = min(metric_data)
    max_val = max(metric_data)
    range_val = max_val-min_val
    return f"{range_val}"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)