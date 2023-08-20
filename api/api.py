from flask import Flask
from log_config import get_logger
from service import get_forecast_summary

log = get_logger()
app = Flask(__name__)


@app.route("/")
def get_forecast():
    result = get_forecast_summary()
    log.debug(result)
    return result
