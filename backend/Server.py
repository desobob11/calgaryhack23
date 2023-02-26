from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import flask
import json
from Database import Database
from Plotter import Plotter
import sqlite3
import base64
from io import StringIO, BytesIO
app = Flask(__name__, static_folder="jsons")
CORS(app)

with open("jsons/figure/img.png", "wb+") as file:
    pass
Database.load_jsons()
active_data = None
class Application:



    def __init__(self):
        self._active_data = None

    



    @app.route("/")
    def home_page():
        return "<div>home page</div>"
    





    @app.route('/jsons/regions_data.json/', methods=["POST", "GET"])
    @cross_origin()
    def send_region_json():
        payload = None
        with open ("jsons/regions_data.json", "r") as file:
            payload = json.load(file)
        return jsonify(payload)
    
    @app.route('/jsons/series_data.json/', methods=["POST", "GET"])
    @cross_origin()
    def send_series_json():
        payload = None
        with open ("jsons/series_data.json", "r") as file:
            payload = json.load(file)
        return jsonify(payload)
    
    @app.route('/jsons/', methods=["POST", "GET"])
    @cross_origin()
    def get_selected_series():
        active_data = request.json
        con = sqlite3.connect("gen_data.db")

        pulled_data = Database.load_data(con, active_data)

        plotter = Plotter(pulled_data)
        plotter.line(active_data)
        plotter.save_fig()
        plotter._data = {}
        return "<div> Request received </div>"
    
    @app.route('/jsons/figure/', methods=["POST", "GET"])
    @cross_origin()
    def send_figure():
        png_output = StringIO()
       # img_data = None
        with open("jsons/figure/img.png", "rb") as file:
            img_data = file.read()
            print(img_data)
            b64 = base64.b64encode(img_data).decode("unicode_escape")
            print(b64)
            #return "<div> Get figure </div>"
            return jsonify({"png_string": b64})


    @app.route('/jsons/clear/', methods=["POST", "GET"])
    @cross_origin()
    def clear_data():
        return



