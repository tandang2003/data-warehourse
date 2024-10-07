import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

# Get the root directory dynamically
ROOT_DIR = Path(__file__).parent.parent.parent
PATH_ENV = os.path.join(ROOT_DIR, ".env")
load_dotenv(dotenv_path=PATH_ENV)
config = dotenv_values(PATH_ENV)
SOURCE_A_URL = config["SOURCE_A_URL"]

DRIVER_PATH = os.path.join(ROOT_DIR, "driver/chromedriver-linux64/chromedriver")
U_BLOCK = os.path.join(ROOT_DIR, "driver/chromedriver-linux64/uBlock.crx")

FOLDER_DATA = os.path.join(ROOT_DIR, "data")
