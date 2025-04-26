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
        <a href="/stats/device/cpu"><button>CPU Statistics</button></a>
        <a href="/stats/device/gpu"><button>GPU Statistics</button></a>
        <a href="/stats/device/ram"><button>RAM Statistics</button></a>
        <a href="/"><button>Home</button></a>
    """


@app.route("/device/<device>")
def device_stats(device):
    metrics = ["temperature", "load", "speed"]
    stats_dict = {}

    for m in metrics:
        data = get_data(device, m)
        if data:
            stats_dict[m] = {
                "device": device,
                "stat": m,
                "minimum": min(data),
                "maximum": max(data),
                "mean": sum(data) / len(data),
                "range": max(data) - min(data)
            }
        else:
            stats_dict[m] = "No data found"

    return render_template("stats.html", stats_dict=stats_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)