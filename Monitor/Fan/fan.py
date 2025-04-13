import random
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@app.route('/')
def fan():
    return 'FAN SPEED MONITORING: Enter a device to continue\n'


# Route to handle device specific statistics
@app.route('/device')
def fan_device():
    fan_speed = random.randint(0, 5000)
    return f'GPU Fan speed = {fan_speed} RPM\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5252)
