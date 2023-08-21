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


def filter_list_to_date_time(object_list, date_time: datetime):
    """
    Filters an object list to zero or one entry matching the current date time
    """
    for object in object_list:
        object_date_time = datetime.strptime(object["Datetime"], "%Y-%m-%d %H:%M:%S")
        if _is_datetime_within_3_hours_from(
            date_time_to_window=object_date_time, date_time_to_check=date_time
        ):
            return [object]

    return None


def _is_datetime_within_3_hours_from(
    date_time_to_window: datetime, date_time_to_check: datetime
):
    """
    Checks of date_time_to_check is within a window of +3 hours from the date_time_to_window
    """
    window_start = date_time_to_window
    window_end = date_time_to_window + timedelta(hours=3)
    return date_time_to_check >= window_start and date_time_to_check < window_end


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
