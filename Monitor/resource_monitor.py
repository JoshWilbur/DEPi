import requests
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    return cache.incr('hits')


@app.route('/')
def index():
    fan_speed = requests.get("http://fan:5252/device")
    page_hits = get_hit_count()
    return f"""
        Please enter a device to monitor. Options are: CPU, GPU, PS <br>
        Page accesses: {page_hits} <br>
        {fan_speed.text}<br>
        """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
