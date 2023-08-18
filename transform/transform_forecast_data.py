from datetime import datetime, timedelta


def transform_to_list_of_json(data):
    """
    Returns the weather forecast for each datetime is an object list that looks like:
    [
        {"Datetime": "2023-08-16 09:00:00", "Wind Gust (mph)": "27", "Temperature (C)": "25", ... },
        {...}
    ]
    """
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

    return object_list, object_keys


def filter_list_to_current_date_time(object_list):
    """
    Filters an object list to zero or one entry matching the current date time
    """
    for object in object_list:
        nowDateTime = datetime.now()
        objectDateTime = datetime.strptime(object["Datetime"], "%Y-%m-%d %H:%M:%S")
        windowStart = objectDateTime
        windowEnd = objectDateTime + timedelta(hours=3)
        if nowDateTime >= windowStart and nowDateTime < windowEnd:
            return [object]

    return []


def _forecastPropertyCodeMappings(data):
    """
    Creates an accessible data structure to lookup label for a forecast property code i.e.
    {
       "G": "Wind Gust (mph)"
        ...
    }
    """
    codeMappings = {}
    for code in data["SiteRep"]["Wx"]["Param"]:
        code_name = code["name"]
        codeMappings[code_name] = {
            "name": f"""{code["$"]} ({code["units"]})""",
        }
    return codeMappings
