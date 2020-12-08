import sqlalchemy
from datetime import timedelta
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import json
from flask import Flask, jsonify
#setting up the JSON for precipitation

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
session=Session(engine)

measurement=Base.classes.measurement
station=Base.classes.station
  
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        )

@app.route("/api/v1.0/precipitation")
def precip():
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    precp = {date:prcp for date,prcp in results}
    return precp

@app.route("/api/v1.0/stations")
def places():
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def observations():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    most_active = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    active_station = session.query(measurement.station).filter(measurement.station == most_active[0][0]).all()
    dates_temps = session.query(measurement.date).filter(measurement.date >= prev_year),(measurement.tobs).filter(measurement.tobs >=prev_year).all()
    session.close()
    #last_station = {station:date for sta,final_data in }
    #print(active_station)
    print(dates_temps)
    #results = list(np.ravel(last_station))
    return (last_station)


@app.route("/api/v1.0/<start>") 
def date_temp(start_date=None, end_date=None):
    if start_date is None:
        temps = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).all()
    else:
        temps = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    return temps
    print(temps)

@app.route("/api/v1.0/<start>/<end>")
def averages(temps, end_date=None):
    if end_date is None:
        temps = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).all()
    else:
        temps = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
        temps_json=json.dumps(temps)
    return temps_json
    


if __name__ == "__main__":
    app.run(debug=True)