import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import platform

# Data config
# Get the root directory dynamically

ROOT_DIR = Path(__file__).parent.parent.parent
FOLDER_DATA = os.path.join(ROOT_DIR, "data")

PATH_ENV = os.path.join(ROOT_DIR, ".env")
PATH_ENV_DEV = os.path.join(ROOT_DIR, ".env.dev")

load_dotenv(dotenv_path=PATH_ENV)
load_dotenv(dotenv_path=PATH_ENV_DEV, override=True)

config = dotenv_values(PATH_ENV)
os_name = platform.system()
SOURCE_A_BASE = config["SOURCE_A_BASE"]
SOURCE_A_1 = config["SOURCE_A_1"]
SOURCE_A_2 = config["SOURCE_A_2"]
SOURCE_B_BASE = config["SOURCE_B_BASE"]
SOURCE_B_1 = config["SOURCE_B_1"]
SOURCE_B_2 = config["SOURCE_B_2"]
SOURCE_B_3 = config["SOURCE_B_3"]
LIMIT_ITEM = int(config["LIMIT_ITEM"])
LIMIT_PAGE = int(config["LIMIT_PAGE"])

