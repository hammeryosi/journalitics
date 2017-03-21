from flask import Flask, render_template, jsonify
import os
from getData import fetch

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/name-count-for-time-range_<start>_<end>')
def getCountsPerTimeRange(start, end):
    data = fetch.getTopNameCount(start, end)
    return jsonify(result=data)

@app.route('/name-list-for-time-range_<start>_<end>_<n>')
def getNamesForTimeRange(start, end, n):
    data = fetch.getTopNames(start, end, n)
    return jsonify(result=data)

@app.route('/time-range')
def timeRangeSearch():
    return render_template('time-range-search.html')

@app.route('/links')
def links():
    return render_template('links.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)