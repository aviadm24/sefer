import requests
import json


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


# url = "http://www.sefaria.org/api/index"
# response = requests.get(url)
# response.raise_for_status()
with open("index.json", encoding="utf-8") as f:
    print(f.read())
#     myJson = json.load(f.read())
# val = json_extract(myJson, "title")
# print(val)