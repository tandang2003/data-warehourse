# Crawl data etate by Python

## Overview

Tool cào dữ liệu cho trang web 'https://batdongsan.com.vn'

## Table of Contents

[//]: # ()
[//]: # (- [Prerequisites]&#40;#prerequisites&#41;)

[//]: # (- [Installation]&#40;#installation&#41;)

[//]: # (- [Setup]&#40;#setup&#41;)

[//]: # (- [Running the Project]&#40;#running-the-project&#41;)

[//]: # (- [Usage]&#40;#usage&#41;)

[//]: # (- [Contributing]&#40;#contributing&#41;)

[//]: # (- [License]&#40;#license&#41;)

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Git
- Chrome Browser version 129.0.6668.100

## Optional

### Install Web Driver Chrome
   - Kiểm tra phiên bản chrome của máy bạn bằng cách vào chrome -> Help -> About Google Chrome
     ![img.png](doc/img.png)
   - Tải Chrome webdriver tại [đây](https://googlechromelabs.github.io/chrome-for-testing)
   - Giải nén và copy file chromedriver.exe vào thư mục driver chứa file crawl.py (đối với windows)
   - Chỉnh sửa path lưu web driver trong file crawl.py

## Setup
### 1. Install environment
```bash
   python3 -m venv .venv
```

### 2. Activate environment and install requirements
#### Windows
```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
```
#### Ubuntu
```bash
   source .venv/bin/activate
   pip install -r requirements.txt
```

### 3. Run the project (in root project)
```bash
  python3 -m  src.main
```