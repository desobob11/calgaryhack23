from flask import Flask
from flask import request
import flask
import json
from flask_cors import CORS
from Database import Database
import sqlite3 as sql3
import sqlalchemy as sql


app = Flask(__name__)
CORS(app)

con = sql3.connect("gen_data.db")
cursor = con.cursor()


@app.route("/jsons", methods=["GET"])
def data():
    Database.load_jsons()

    with open("jsons/series_data.json", "r") as file:
        series = json.load(file)

    with open("jsons/regions_data.json", "r") as file:
        regions = json.load(file)

    response = {
        "series": series,
        "regions": regions,
        "status": "success"
        
    }
    return response
    
if __name__ == "__main__":
    app.run("localhost", 6969, debug=True)