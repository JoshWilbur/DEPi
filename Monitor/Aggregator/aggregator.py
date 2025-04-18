import redis
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET'])
def aggregator():
    devices = cache.keys("device:*")
    output = "<h2>TEST</h2>"
    for d in devices:
        data = cache.hgetall(d)
        output += f"<p><b>{d}</b>: Temp={data.get('temperature')}, Load={data.get('load')}</p>"
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
