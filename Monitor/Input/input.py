import redis
from flask import Flask, render_template, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route('/', methods=["GET", "POST"])
def data_entry():
    if request.method == "POST":
        device_name = request.form.get("device")
        temperature = request.form.get("temperature")
        load = request.form.get("load")

        # Ensure temp and load data are numbers, then post
        if temperature.isnumeric() and load.isnumeric():
            cache.hset(f"device:{device_name}", mapping={
                "temperature": temperature,
                "load": load
            })
            return f"{device_name} data posted successfully"
        else:
            return "Error saving data"

    return render_template("./input.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
