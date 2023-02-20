from flask import Flask, render_template
import json





app = Flask(__name__, template_folder="WebApp", static_folder="static")

query_data = None

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/getmethod/<jsdata>')
def get_js_data(jsdata):
    return jsdata