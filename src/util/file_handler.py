import pandas as pd
import os
import json

from exceptiongroup import catch

from src.config import FOLDER_DATA


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
