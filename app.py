from flask import Flask, request
from flask import render_template
from datetime import datetime, timedelta
import json
from package import model

app = Flask(__name__)

@app.route("/")
def index():
    min_day = datetime.today() + timedelta(days=1)
    min_day = min_day.strftime("%Y-%m-%d")

    max_day = datetime.today() + timedelta(days=5)
    max_day = max_day.strftime("%Y-%m-%d")
   
    return render_template('index.html',min_day=min_day, max_day=max_day)

@app.route('/predictions',  methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        # TODO: Girdiler kontrol edilmeli
        reason = request.form['reason']
        maintenance_day = request.form['maintenance_day']
        maintenance_day = datetime.strptime(maintenance_day,"%Y-%m-%d" )
        
        mlmodel_object = model.MLModel(date=maintenance_day.strftime("%Y-%m-%d"))
        # TODO: Prediction queue'ya atılmalı ve asenkron yapılmalı. Bkz. HTTP Request Timeout
        data = mlmodel_object.predict()
        print(data['is_holiday'])

        return render_template('predictions.html', data=data, reason=reason, maintenance_day=maintenance_day)

@app.route('/schedule',  methods=['GET', 'POST'])
def schedule():
    # TODO: Form Validation yapılmalı,
    maintenance_type= request.form['maintenance_type']
    day = request.form['maintenance_day']
    reason = request.form['reason']
    district = request.form['district']
    neighborhood = request.form['neighborhood']
    street = request.form['street']

    maintenance_hours = request.form.getlist('maintenance_hours')
    
    maintenance_hours_map = map(lambda hour:int(hour), maintenance_hours)
    maintenance_hours = list(maintenance_hours_map)

    start_time = min(maintenance_hours)
    end_time = max(maintenance_hours) + 1
    total_time = end_time - start_time
    return render_template('schedule.html', day=day, reason=reason, district=district, 
                                            neighborhood=neighborhood, street=street,
                                            maintenance_type=maintenance_type, start_time=start_time,
                                            end_time=end_time, total_time=total_time) 

@app.route('/calendar')
def calendar():
    return render_template("calendar.html")

@app.route('/about')
def about():
    # TODO: Buradaki JSON'ı kaldırıp, içeriye alabiliriz. 
    with open('public/team.json', 'r') as team:
            team = json.load(team)
    return render_template('about.html', team=team)
