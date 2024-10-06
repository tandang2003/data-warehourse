import os
from pathlib import Path

# Get the root directory dynamically
ROOT_DIR = Path(__file__).parent.parent

SOURCE_A_URL = 'https://batdongsan.com.vn/nha-dat-cho-thue-an-giang'

DRIVER_PATH = CHROMEDRIVER_PATH = os.path.join(ROOT_DIR, "driver/chromedriver-linux64/chromedriver")

FOLDER_DATA = os.path.join(ROOT_DIR, "data")
