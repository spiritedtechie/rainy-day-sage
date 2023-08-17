from datetime import datetime, timedelta


# Returns the weather forecast for each datetime is an object list that looks like:
# [
#   {"Datetime": "2023-08-16 09:00:00", "Wind Gust (mph)": "27", "Temperature (C)": "25", ... },
#   {...}
# ]
def transform_data(data):
    codeMappings = _forecastPropertyCodeMappings(data)

    object_keys = []
    object_list = []

    object_keys.append("Datetime")
    for i in codeMappings.values():
        object_keys.append(i["name"])

    for period in data["SiteRep"]["DV"]["Location"]["Period"]:
        dateText = period["value"]

        threeHourlyBlock = period["Rep"]
        for block in threeHourlyBlock:
            minutesFromMidnight = int(block["$"])
            dateTime = datetime.strptime(dateText, "%Y-%m-%dZ")
            dateTime = dateTime + timedelta(minutes=minutesFromMidnight)

            forecastObj = {}
            forecastObj["Datetime"] = dateTime.strftime("%Y-%m-%d %H:%M:%S")

            for key in block.keys():
                if key != "$":
                    forecastObj[codeMappings[key]["name"]] = block[key]

            object_list.append(forecastObj)

    # print(object_keys)
    # print(object_list)

    return object_list, object_keys


# Creates an accessible data structure to lookup label for a forecast property code i.e.
#
# {
#   "G": "Wind Gust (mph)"
#   ...
# }
#
def _forecastPropertyCodeMappings(data):
    codeMappings = {}
    for code in data["SiteRep"]["Wx"]["Param"]:
        code_name = code["name"]
        codeMappings[code_name] = {
            "name": f"""{code["$"]} ({code["units"]})""",
        }
    return codeMappings
