import datetime as dt
import json

from flask import Flask
from flask import jsonify


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "ts": dt.datetime.now(),
    })


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', threaded=True)