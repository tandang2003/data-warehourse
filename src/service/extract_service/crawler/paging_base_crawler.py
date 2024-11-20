import json
from abc import abstractmethod
from datetime import datetime

from selenium.common import WebDriverException, NoSuchElementException

from src.service.extract_service.crawler.base_crawler import BaseCrawler
from src.util.validation_util import check_url_valid


class PagingBase(BaseCrawler):

    def __init__(self,
                 limit_page,
                 format_file,
                 extension,
                 prefix,
                 dir_path,
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
        self._dir_path = dir_path
        self._purpose = purpose
        self._base_url = base_url
        self._source_page = source_page
        self._paging_pattern = paging_pattern
        self._current_page = 1
        self._scenario = json.loads(scenario)
        self._navigate_scenario = json.loads(navigate_scenario)
        # # Chứa danh sách url item
        self._list_url = []
        # Chứa danh sách item đã cào được
        self._list_item = []

    # TODO trả về 1 dict vs  _file_name VARCHAR(200), _error_file_name VARCHAR(200), _count_row INT,
    #                                     _status VARCHAR(200),
    def handle(self):
        super().setup_driver(headless=True)
        self.before_run()

        for (page) in range(1, 1 + self._limit_page):
            list_url = self.crawl_page(page)
            list_item_each_page = []
            for (url) in list_url:
                try:
                    if not check_url_valid(url):
                        raise NameError
                    item_crawled = self.crawl_item(url, self._scenario)
                    print(item_crawled)
                    self._list_item.append(item_crawled)
                    self.after_run_each_item(item_crawled)
                except NameError:
                    self.handle_error_item(NameError)
            self.after_run_each_page(list_item_each_page)
            list_item_each_page.clear()
            self._current_page += 1
        print(self._list_item)
        self.after_run()

    def crawl_item(self, url, scenario):
        try:
            self.get_url(url)

            print(f"Visiting item: {url}")

            self.wait(10)
            current_url = self.driver.current_url
            if current_url != url:
                return None

            driver = self.driver.page_source
            self.clean_html(driver)
            result = {}

            for field_name, properties in scenario.items():
                print(f"Field Name: {field_name}")
                print(f"Properties: {properties}")
                result[field_name] = self.find_element_by_config(properties)

            return result
        except WebDriverException as e:
            return None

    def crawl_page(self, page):
        url_page = f"{self._base_url}/p{page}"
        print(f"Visiting page: {url_page}")
        self.get_url(url_page)

        self.wait(5)
        driver = self.driver.page_source
        self.clean_html(driver)

        estate_list = self.soup.select(self._navigate_scenario["link"])
        list_url = []
        for (estate) in estate_list:
            link = estate.select_one(self._navigate_scenario["item"]).get("href")
            if link.startswith("https://"):
                continue
            else:
                list_url.append(f"{self._base_url}{str(link)}")
        return list_url

    def before_run(self):
        pass

    def after_run(self):
        pass

    def after_run_each_page(self, list_item):
        pass

    def after_run_each_item(self, item):
        pass

    def handle_error_item(self, error):
        pass

    def find_element_by_config(self, field_properties):
        print(field_properties)
        method = field_properties.get("method", None)
        selector = field_properties.get("selector", None)
        attribute = field_properties.get("attribute", None)
        quantity = field_properties.get("quantity", 0)
        xpath = self.find_elements_with_xpath(selector)

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
