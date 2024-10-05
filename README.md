# Hướng dẫn
## Cài đặt 
- Cài đặt python version 3 trở lên 
- Install selenium 
- Install webdriver của google chrome
- Chỉnh sửa url trong file crawl.py
```
  6  url = 'https://batdongsan.com.vn/nha-dat-cho-thue-an-giang'
```

## Cài đặt Chrome webdriver
- Kiểm tra phiên bản chrome của máy bạn bằng cách vào chrome -> Help -> About Google Chrome
    ![img.png](doc/img.png)
- Tải Chrome webdriver tại [đây](https://googlechromelabs.github.io/chrome-for-testing)
- Giải nén và copy file chromedriver.exe vào thư mục driver chứa file crawl.py (đối với windows)
- Chỉnh sửa path lưu web driver trong file crawl.py
```
  7  path = 'C:/Users/DELL/Desktop/Python/Project/RealEstateCrawler/data/'
```