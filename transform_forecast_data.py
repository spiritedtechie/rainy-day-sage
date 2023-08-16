import json
from datetime import datetime, timedelta


# Weather forecast for each datetime is an object list that looks like:
# [
#   {"Datetime": "2023-08-16 09:00:00", "Wind Gust (mph)": "27", "Temperature (C)": "25", ... },
#   {...}
# ]
def transform_data(data):

    # An accessible data structure to lookup fullname & units for a forecast variable's code
    codeMappings = {}
    for code in data["SiteRep"]["Wx"]["Param"]:
        code_name = code["name"]
        codeMappings[code_name] = {
            "units": code["units"],
            "full_name": code["$"],
            "column_name": f"""{code["$"]} ({code["units"]})""",
        }

    object_keys = []
    object_list = []
    object_keys.append("Datetime")
    for i in codeMappings.values():
        object_keys.append(i["column_name"])

    for period in data["SiteRep"]["DV"]["Location"]["Period"]:
        dateText = period["value"]

        threeHourlyChunk = period["Rep"]
        for chunk in threeHourlyChunk:
            minutesFromMidnight = int(chunk["$"])
            dateTime = datetime.strptime(dateText, "%Y-%m-%dZ")
            dateTime = dateTime + timedelta(minutes=minutesFromMidnight)

            forecastObj = {}
            forecastObj["Datetime"] = dateTime.strftime("%Y-%m-%d %H:%M:%S")

            for key in chunk.keys():
                if key != "$":
                    forecastObj[codeMappings[key]["column_name"]] = chunk[key]

            object_list.append(forecastObj)

    # print(object_keys)
    # print(object_list)

    return object_list, object_keys
