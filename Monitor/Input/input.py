import redis
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@app.route('/', methods=["GET", "POST"])
def data_entry():
    if request.method == "POST":
        device_name = request.form.get("device")
        temperature = request.form.get("temperature")
        load = request.form.get("load")

        # Post data to redis
        cache.hset(f"device:{device_name}", mapping={
            "temperature": temperature,
            "load": load
        })

    return render_template("./input.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
