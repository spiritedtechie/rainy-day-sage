import csv
import io


def convert_to_csv(object_list: list[dict], object_keys: list[str]):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=object_keys, delimiter=",")
    writer.writeheader()
    writer.writerows(object_list)
    return output.getvalue()
