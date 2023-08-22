import csv
from datetime import datetime, timedelta
from io import StringIO


def transform(data):
    # Extract parameters from data
    parameters = data["SiteRep"]["Wx"]["Param"]
    parameter_names = [
        f"{param['$']} - {param['units']}" for param in parameters
    ]

    # Get the current datetime
    current_datetime = datetime.now()

    # Extract periods from data
    location = data["SiteRep"]["DV"]["Location"]
    periods = location["Period"]

    # Define a generator function to yield CSV rows
    def generate_csv_rows():
        yield ["Datetime"] + parameter_names
        for period in periods:
            period_date = datetime.strptime(period["value"], "%Y-%m-%dZ")
            for rep in period["Rep"]:
                period_datetime = period_date + timedelta(minutes=int(rep["$"]))
                if period_datetime <= current_datetime < period_datetime + timedelta(hours=3):
                    values = [rep.get(param["name"]) for param in parameters]
                    yield [period_datetime.strftime("%Y-%m-%d %H:%M:%S")] + values

    # Use the generator to create an in-memory string buffer
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerows(generate_csv_rows())

    # Get the CSV data as a string
    csv_data = csv_buffer.getvalue()

    return csv_data
