import json
import logging
import os.path
import re
from datetime import datetime

from selenium.common import WebDriverException, NoSuchElementException

from src.service.AppException import AppException, handle_app_exception, LEVEL
from src.service.extract_service.crawler.base_crawler import BaseCrawler
from src.util.file_util import write_json_to_csv
from src.util.validation_util import check_url_valid


class PagingBase(BaseCrawler):

    def __init__(self,
                 limit_page,
                 format_file,
                 extension,
                 prefix,
                 data_dir_path,
                 error_dir_path,
                 purpose,
                 base_url,
                 source_page,
                 paging_pattern,
                 scenario,
                 navigate_scenario):
        super().__init__()
        self._limit_page = limit_page
        self._format_file = format_file
        self._extension = extension
        self._prefix = prefix
        self._data_dir_path = data_dir_path
        self._error_dir_path = error_dir_path
        self._purpose = purpose
        self._base_url = base_url
        self._source_page = source_page
        self._paging_pattern = paging_pattern
        self._scenario = json.loads(scenario)
        self._navigate_scenario = json.loads(navigate_scenario)
        # # Chứa danh sách url item
        self._list_url = []
        # Chứa danh sách item đã cào được
        self._list_item = []

    # 7
    def handle(self) -> dict:
        # 7.1 Thực hiện tạo cấu hình crawler(selenium) bằng hàm setup_driver (8)
        super().setup_driver(headless=True)
        try:
            for (page) in range(1, 1 + self._limit_page):
                # 7.2. Thực hiện gọi hàm crawl_page (9) để lấy danh sách các url item trong trang
                list_url = self.crawl_page(page)
                # 7.3. Lấy 1 url item từ trong danh sách các item có trong trang
                for (url) in list_url:
                    # 7.4 Kiểm tra url có hợp lệ không
                    if not check_url_valid(url):
                        # 7.4.1 Không hợp lệ
                        break
                    # 7.4.2 Hợp lệ
                    # 7.5.thực hiện gọi hàm crawl_item để lấy các thông tin của item
                    item_crawled = self.crawl_item(url, self._scenario)
                    print(item_crawled)
                    # 7.6.Thêm các thông tin lấy được vào danh sách
                    self._list_item.append(item_crawled)
            logging.info(self._list_item)
            # 7.7 gọi hàm handle_success() đễ xử lý thành công
            return self.handle_success()
        except AppException as e:
            # 7.8 Gọi hàm handle_exception() để xử lý lỗi
            return self.handle_exception(e)

    def crawl_item(self, url, scenario):
        try:
            # gọi request đến url chi tiết bất động sản
            self.get_url(url)

            logging.info(f"Visiting item: {url}")

            self.wait(10)
            current_url = self.driver.current_url
            if current_url != url:
                return None

            driver = self.driver.page_source

            # Xóa các thẻ không cần thiết
            self.clean_html(driver)
            result = {}

            for field_name, properties in scenario.items():
                result[field_name] = self.find_element_by_config(properties)

            return result
        except WebDriverException as e:
            return None

    def crawl_page(self, page):
        url_page = f"{self._base_url}/{self._source_page}{self._paging_pattern}{page}"
        print(f"Visiting page: {url_page}")

        # Lấy HTML từ url
        self.get_url(url_page)
        self.wait(5)
        driver = self.driver.page_source

        # Lọc các tag không sử dụng
        self.clean_html(driver)

        estate_list = self.soup.select(self._navigate_scenario["list"])
        list_url = []

        if len(estate_list) == 0:
            raise AppException(LEVEL.FILE_ERROR, "No data found")
        for (estate) in estate_list:
            link = estate.select_one(self._navigate_scenario["item"]).get("href")
            if link.startswith("https://"):
                continue
            else:
                list_url.append(f"{self._base_url}{str(link)}")
        return list_url

    def before_run(self):
        pass

    def handle_success(self):
        data = self._list_item
        current_date = datetime.now().strftime(self._format_file)
        filename = f"{self._prefix}{current_date}.{self._extension}"
        path = os.path.join(self._data_dir_path, filename)
        write_json_to_csv(path, data)
        logging.info(f"Data has been saved to {path}")
        return {
            'file': path,
            'count_row': len(data),
            'status': 'STAGING_PENDING',
            'error_file_name': None
        }

    def handle_exception(self, exception: AppException):
        filename = f"{self._prefix}{self._format_file}.log"
        path = os.path.join(self._error_dir_path, filename)
        handle_app_exception(exception, path)
        return {
            'file': None,
            'error_file_name': path,
            'count_row': 0,
            'status': 'STAGING_ERROR'
        }

    def find_element_by_config(self, field_properties):
        # print(field_properties)
        method = field_properties.get("method", None)
        selector = field_properties.get("selector", None)
        attribute = field_properties.get("attribute", None)
        quantity = field_properties.get("quantity", 0)
        regex = field_properties.get("regex", None)
        xpath = self.find_elements_with_xpath(selector)

        try:
            if regex:
                return self.find_element_by_regex(xpath, regex)
            if quantity is None:
                return list(map(lambda img: img.get(attribute), xpath)) if xpath else None
            quantity -= 1
            if method == "time":
                return datetime.now().strftime("%d/%m/%Y")
            if method == "url":
                return self.driver.current_url
            if method == "description":
                return ''.join(xpath[quantity].itertext()).strip() if xpath else None
            if method == "get_attribute":
                return xpath[quantity].get(attribute) if xpath else None
            if method == "text":
                return xpath[quantity].text if xpath else None
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def find_elements_with_xpath(self, xpath):
        try:
            elements = self.etree.xpath(xpath)

            if not elements:
                print("No elements found with the specified XPath.")
            return elements

        except NoSuchElementException:
            print("Element not found using the provided XPath.")
            return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def find_element_by_regex(self, xpath, regex_pattern):
        id_pattern = fr"{regex_pattern}".replace("\\\\", "\\")
        text = xpath[0].text_content().strip()
        print(f'nk{text}')
        match = re.search(id_pattern, text)
        if match:
            return match.group(1)
        return None

# if __name__ == '__main__':
#     from lxml import html
#
#     # The provided HTML
#     html_content = """
#    <div class="sc-6orc5o-15 jiDXp"><h1>Bán nhà 100m2 Nguyễn Trãi, Q.1 chỉ 23,9 tỷ</h1><div class="sc-6orc5o-16 jGIyZP"><div class="price">23,9 tỷ</div></div><div class="address"><span class="sc-1vo1n72-6 bZuuMO"></span>212/12, Đường Nguyễn Trãi, Phường Nguyễn Cư Trinh, Quận 1, TP.HCM</div><div class="date"><span class="sc-1vo1n72-7 fGnMSX"></span>Ngày đăng: <!-- -->Hôm nay<!-- --> - Mã tin: <!-- -->69527925</div></div>
#     """
#
#     # Parse the HTML string
#     tree = html.fromstring(html_content)
#
#     # Corrected XPath to select the div with class "date"
#     xpath = tree.xpath("//*[contains(@class, 'sc-6orc5o-15 jiDXp')]//*[@class='date']")
#
#     # Extract and print the text content
#     if xpath:
#         print(xpath[0].text_content().strip())
#     else:
#         print("No matching element found.")
