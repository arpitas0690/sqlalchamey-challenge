# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, inspect, func, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>;<br/>"
        f"/api/v1.0/<start>/<end>;"
    )

#################################################
# Database Setup
#################################################

#This is for the precipitation dateset

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Return a list """
    # Query results from precipitation analysis(i.e. retrieve only the 12 months of data) to a dictionary.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.date,measurement.prcp).\
    filter(measurement.date >=year_ago).\
    order_by(measurement.date).all()
    
    session.close()

    # Create a dictionary from the data
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)


    # Convert list of tuples into normal list
    precipitation_list = list(np.ravel(results))

    return jsonify(precipitation_list)


#This is for the station dateset

@app.route("/api/v1.0/stations")
def stations():
    #Create our session(link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    #Query all results from stations dataset
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs(): 
    #Create our session (link) from Python to the DB
    session = Session(engine)

    """Return results for dates and temperature observations for the most active station for the previous year"""
    # Query the dates and temperature observations of the most-active station for the previous year of data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.tobs).\
    filter((measurement.date >=year_ago) & (measurement.station == 'USC00519281')).\
    order_by(measurement.date).all()

    session.close()

    #Convert list of tuples into normal list
    temperature_list = list(np.ravel(results))

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def temperature1(start):
    #Create our session (link) from Python to the DB
    session = Session(engine)

    "Return list of minimum temperature, the average temp, and maximum temperature for a specificed start and end range"
    #Query max, min, avg temps
    start = dt.date(2016, 8, 23)
    results = session.query(func.min(measurement.tobs).label("min_temp"),
                            func.avg(measurement.tobs).label("avg_temp"),
                            func.max(measurement.tobs).label("max_temp")).\
    filter(measurement.date >= start).\
    order_by(measurement.date).all()

    session.close()



    #Convert list into a normal list
    temperature_stats1 = {
     "start_date": start.strftime('%Y-%m-%d'),
     "TMIN": results[0].min_temp,
     "TAVG": results[0].avg_temp,
     "TMAX": results[0].max_temp
    }

    # Return the JSON response
    return jsonify(temperature_stats1)

@app.route("/api/v1.0/<start>/<end>")
def temperature2(start, end):
    #Create our session (link) from Python to the DB
    session = Session(engine)

    "Return list of minimum temperature, the average temp, and maximum temperature for a specificed start and end range"
    #Query max, min, avg temps
    start= dt.date(2016, 8, 23)
    end= dt.date(2017, 8, 23)
    results = session.query(func.min(measurement.tobs).label("min_temp"),
                            func.avg(measurement.tobs).label("avg_temp"),
                            func.max(measurement.tobs).label("max_temp")).\
    filter(measurement.date.between(start,end)).\
    order_by(measurement.date).all()

    session.close()

    #Convert list into a normal list
    temperature_stats2 = {
     "start_date": start.strftime('%Y-%m-%d'),
     "end_date": end.strftime('%Y-%m-%d'),
     "TMIN": results[0].min_temp,
     "TAVG": results[0].avg_temp,
     "TMAX": results[0].max_temp
    }

    # Return the JSON response
    return jsonify(temperature_stats2)


if __name__ == '__main__':
    app.run(debug=True)




