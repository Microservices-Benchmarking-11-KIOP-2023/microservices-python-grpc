import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_store = {}


def load_data():
    data_file = "geo.json"
    json_file = os.path.join(current_dir, data_file)
    try:
        with open(json_file, "r") as file:
            data_store[data_file] = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {data_file} not found in {json_file}")
    except json.JSONDecodeError:
        print(f"Error: File {data_file} is not a valid JSON file")
