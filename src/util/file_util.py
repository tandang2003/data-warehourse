import json
import os

import pandas as pd

from src.config.setting import FOLDER_DATA


def write_to_csv(filename, data):
    """Save a list of dictionaries to a CSV file using Pandas."""
    if not data:
        print("No data to save.")
        return

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    location = os.path.join(FOLDER_DATA, filename)
    if not os.path.exists(location):
        os.makedirs(location)

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False, encoding='utf-8')

    print(f"Data saved to {filename}")


def write_json_to_file(file_name, data):
    location = os.path.join(FOLDER_DATA, file_name)
    json_file = open(location, 'w')
    try:
        json.dump(data, json_file, ensure_ascii=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error: {e}")
    json_file.close()


def read_file_to_json(file_name):
    location = os.path.join(FOLDER_DATA, file_name)
    with open(location, 'r', encoding='utf-8') as file:
        # Load the data from the file and convert it to a Python object
        return json.load(file)


def write_json_to_csv(file_name, json_list):
    """
    Convert nested JSON objects to strings and save the list to a CSV file.

    :param file_name: The name of the CSV file.
    :param json_list: A list of JSON objects to be converted and saved to CSV.
    :param folder_data: The directory where the CSV file will be saved (default: "output_folder").
    """
    # Create the directory if it does not exist
    os.makedirs(FOLDER_DATA, exist_ok=True)
    location = os.path.join(FOLDER_DATA, file_name)
    print(f"Saving CSV to: {location}")

    # Process each item in the json_list
    for index, item in enumerate(json_list):
        if item is not None:  # Check if item is not None
            for key, value in item.items():
                json_list[index][key] = convert_nested_to_string(value)  # Convert nested data to JSON string

    # Create DataFrame from the modified list, filter out None items
    json_list = [item for item in json_list if item is not None]  # Remove None items
    df = pd.DataFrame(json_list)

    # Save the DataFrame to a CSV file
    df.to_csv(location, index=False, encoding='utf-8')


def convert_nested_to_string(data):
    """
    Convert nested JSON objects or lists to JSON strings.

    :param data: A potentially nested JSON object (dict or list).
    :return: The original object or a JSON string if it's nested.
    """
    if isinstance(data, (dict, list)):
        return json.dumps(data, ensure_ascii=False)  # Convert to JSON string
    return data  # Return the original value if not nested
