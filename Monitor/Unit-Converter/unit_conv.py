import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def welcome():
    return "This page will direct users to all available conversions"


@app.route("/f2c")
def F_to_C():
    return "This route will convert fahrenheit to celsius"


@app.route("/c2f")
def C_to_F():
    return "This route will convert celsius to fahrenheit"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)