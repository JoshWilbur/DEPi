import redis
from flask import Flask, render_template

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
        <a href="/stats/device/CPU"><button>CPU Statistics</button></a>
        <a href="/stats/device/GPU"><button>GPU Statistics</button></a>
        <a href="/stats/device/RAM"><button>RAM Statistics</button></a>
        <a href="/"><button>Home</button></a>
    """


@app.route("/device/<device>")
def show_stats(device):
    stats = device_stats(device)
    return render_template("stats.html", stats_dict=stats)


@app.route("/device/<device>/get")
def device_stats(device):
    stats_dict = {}
    metrics = ["temperature", "load", "speed"]

    for m in metrics:
        data = get_data(device, m)
        if data:
            stats_dict[m] = {
                "device": device,
                "stat": m,
                "minimum": min(data),
                "maximum": max(data),
                "mean": round(sum(data) / len(data), 2),
                "range": max(data) - min(data)
            }
        else:
            stats_dict[m] = "No data found"

    return stats_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)