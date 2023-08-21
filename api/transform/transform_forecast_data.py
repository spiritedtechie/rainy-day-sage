from datetime import datetime, timedelta


DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

#
# Version 1 - manually written, non refactored, non optimised
#
# def transform_to_list_of_json(data):
#     """
#     Returns the weather forecast for each datetime as an object list that looks like:
#     [
#         {"Datetime": "2023-08-16 09:00:00", "Wind Gust (mph)": "27", "Temperature (C)": "25", ... },
#         {...}
#     ]
#     """
#     code_mappings = _forecast_code_mappings(data)

#     object_keys = []
#     object_list = []

#     object_keys.append("Datetime")
#     for i in code_mappings.values():
#         object_keys.append(i["name"])

#     for period in data["SiteRep"]["DV"]["Location"]["Period"]:
#         date_text = period["value"]

#         three_hourly_block = period["Rep"]
#         for block in three_hourly_block:
#             minutes_from_midnight = int(block["$"])
#             date_time = datetime.strptime(date_text, "%Y-%m-%dZ")
#             date_time = date_time + timedelta(minutes=minutes_from_midnight)

#             forecast_obj = {}
#             forecast_obj["Datetime"] = date_time.strftime("%Y-%m-%d %H:%M:%S")

#             for key in block.keys():
#                 if key != "$":
#                     forecast_obj[code_mappings[key]["name"]] = block[key]

#             object_list.append(forecast_obj)

#     return object_list, object_keys


# Version 2 - LLM optimised
def transform_to_list_of_json(data):
    def parse_datetime(date_text, mins_from_midnight):
        return datetime.strptime(date_text, "%Y-%m-%dZ") + timedelta(
            minutes=mins_from_midnight
        )

    code_mappings = _forecast_code_mappings(data)

    object_list = (
        {
            "Datetime": parse_datetime(period["value"], int(block["$"])).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            **{
                code_mappings[key]["name"]: value
                for key, value in block.items()
                if key != "$"
            },
        }
        for period in data["SiteRep"]["DV"]["Location"]["Period"]
        for block in period["Rep"]
    )

    object_keys = ["Datetime"] + [value["name"] for value in code_mappings.values()]

    return list(object_list), object_keys


def filter_list_to_date_time(object_list, date_time: datetime):
    """
    Filters an object list to zero or one entry matching the current date time
    """
    target_date_time = date_time

    matching_object = next(
        (
            obj
            for obj in object_list
            if _is_datetime_within_3_hours_from(
                reference_datetime=datetime.strptime(obj["Datetime"], DATE_TIME_FORMAT),
                datetime_to_check=target_date_time,
            )
        ),
        None,  # Default value if no match is found
    )

    return [matching_object] if matching_object else None


def _is_datetime_within_3_hours_from(
    reference_datetime: datetime, datetime_to_check: datetime
):
    """
    Checks if 'datetime_to_check' is within a window of +3 hours from 'reference_datetime'.

    Example:
    reference_datetime = datetime(2023, 8, 21, 12, 0, 0)
    datetime_to_check = datetime(2023, 8, 21, 14, 30, 0)
    result = is_datetime_within_3_hours_from(reference_datetime, datetime_to_check)
    # result will be True
    """
    window_start = reference_datetime
    window_end = window_start + timedelta(hours=3)
    return window_start <= datetime_to_check < window_end


def _forecast_code_mappings(data):
    """
    Creates an accessible data structure to lookup label for a forecast property code i.e.
    {
       "G": "Wind Gust (mph)"
        ...
    }
    """
    code_mappings = {
        code["name"]: {"name": f"{code['$']} ({code['units']})"}
        for code in data["SiteRep"]["Wx"]["Param"]
    }
    return code_mappings
