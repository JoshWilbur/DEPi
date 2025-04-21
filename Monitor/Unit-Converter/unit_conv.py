import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route("/")
def welcome():
    return "This page will direct users to all available conversions"


@app.route("/f2c")
def F_to_C():
    return "This endpoint will convert fahrenheit to celsius"


@app.route("/c2f")
def C_to_F():
    return "This endpoint will convert celsius to fahrenheit"