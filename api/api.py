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


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=3001)
