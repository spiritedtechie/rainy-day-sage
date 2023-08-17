from flask import Flask
from service import get_forecast_summary 

app = Flask(__name__)

@app.route("/")
def hello_world():
    result = get_forecast_summary()
    return result