from flask import Flask, jsonify
from sqlalchemy import create_engine
import datetime as dt

app = Flask(__name__)

engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

@app.route('/')
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    conn = engine.connect()
    # Calculate the date one year from the last date in data
    last_date = conn.execute('SELECT max(date) FROM measurement').fetchone()[0]
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    start_date = last_date - dt.timedelta(days=365)
    
    # Retrieve the last year's data of date and prcp values
    data = conn.execute(f"SELECT date, prcp FROM measurement WHERE date >= '{start_date}'").fetchall()
    
    # Convert to dictionary using date as the key and prcp as the value
    precip_dict = {date: prcp for date, prcp in data}
    
    return jsonify(precip_dict)

@app.route('/api/v1.0/stations')
def stations():
    conn = engine.connect()
    stations = conn.execute("SELECT station FROM station").fetchall()
    stations = [station[0] for station in stations]
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    conn = engine.connect()
    last_date = conn.execute('SELECT max(date) FROM measurement').fetchone()[0]
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    start_date = last_date - dt.timedelta(days=365)

    # Retrieve the last year's data of date and tobs for the most active station
    data = conn.execute(f"SELECT date, tobs FROM measurement WHERE station = 'USC00519281' AND date >= '{start_date}'").fetchall()
    
    # Convert to list of dictionaries for date and tobs
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in data]

    return jsonify(tobs_data)

if __name__ == '__main__':
    app.run(debug=True)