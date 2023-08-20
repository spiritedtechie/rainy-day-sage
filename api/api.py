from flask import Flask
from service import get_forecast_summary 

app = Flask(__name__)

@app.route("/")
def get_forecast():
    result = get_forecast_summary()
    print(result)
    return result