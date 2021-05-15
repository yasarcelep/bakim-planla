from flask import Flask, request
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predictions',  methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        with open('public/test_data.json', 'r') as test_data:
            data = json.load(test_data)     
        return render_template('predictions.html', data=data)

@app.route('/schedule',  methods=['GET', 'POST'])
def schedule():
    return render_template('schedule.html')