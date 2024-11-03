import re
from datetime import datetime

from bs4.element import ResultSet
from selenium.common import WebDriverException, NoSuchElementException

from src.config.setting import SOURCE_B_BASE, SOURCE_B_3, SOURCE_B_1
from src.service.extract_service.crawler.config_crawler import config_crawler_source_B
from src.service.extract_service.crawler.paging_base_crawler import PagingBase
from src.util.file_util import write_json_to_file, write_json_to_csv


class SourceB1Crawler(PagingBase):
    _base_url = SOURCE_B_1
    _domain = SOURCE_B_BASE

    def crawl_page(self, page):
        url_page = f"{self._base_url}?page={page}"
        print(f"Visiting page: {url_page}")
        self.get_url(url_page)

        # Wait for 5 seconds
        self.wait(5)
        driver = self.driver.page_source
        self.clean_html(driver)

        estate_list = self.soup.select(".sc-q9qagu-4.iZrvBN")
        list_url = []
        for (estate) in estate_list:
            link = estate.select_one("a.title").get("href")
            list_url.append(f"{self._domain}{str(link)}")
        return list_url

    def crawl_item(self, url):
        super().crawl_item(url)
        result = {}

        for field_name, properties in config_crawler_source_B.items():
            print(f"Field Name: {field_name}")
            print(f"Properties: {properties}")
            result[field_name] = self.find_element_by_config(properties)

        return result

    def __extract_imgs(self):
        tag_img = self.soup.select(".sc-6orc5o-3.ljaVcC img")
        result = []
        for img in tag_img:
            result.append(img.get("data-src"))
        return result

    def base_url(self):
        return self._base_url

    def __extract_properties(self):
        properties = {}
        list_label_attribute: ResultSet = self.soup.select('ul.sc-6orc5o-24.jhtUTo li')

        for item in list_label_attribute:
            spans: ResultSet = item.select("span")
            properties[spans[0].get_text()] = spans[1].get_text()
        price = self.soup.select_one(".sc-6orc5o-15.jiDXp div.price").get_text(strip=True)
        properties["price"] = price
        return properties

    def __extract_user(self):
        return {"phone": self.soup.select_one("span.sc-lohvv8-15.fyGvhT").get_text(strip=True),
                "avatar ": self.soup.select_one(".sc-lohvv8-2.ficBQz img").get("src"),
                "name": self.soup.select_one("span.title").get_text(strip=True)
                }

    def _extract_created_at(self, text):
        created_at_pattern = r"Ngày đăng:\s*([^\-]+)"
        created_at_match = re.search(created_at_pattern, text)
        if created_at_match:
            return created_at_match.group(1).strip()
        return None

        # Function to extract the post ID

    def _extract_post_id(self, text):
        id_pattern = r"Mã tin:\s*(\d+)"
        id_match = re.search(id_pattern, text)
        if id_match:
            return id_match.group(1)
        return None

    def after_run(self):
        data = self._list_item
        current_date = datetime.now().strftime("%Y_%m_%d__%H_%M")
        print(data)
        write_json_to_file(f"source_2_{current_date}.json", data)
        filename = f"source_2_{current_date}.csv"
        write_json_to_csv(filename, data)
        print(f"Data has been saved to {filename}")

    def handle_error_item(self, error):
        super().handle_error_item(error)

    def find_elements_with_xpath(self, xpath):
        try:
            # Attempt to find elements using the provided XPath
            elements = self.etree.xpath(xpath)

            if not elements:
                print("No elements found with the specified XPath.")

            return elements  # Return found elements (can be an empty list if none found)

        except NoSuchElementException:
            print("Element not found using the provided XPath.")
            return []  # Return an empty list on exception

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []  # Return an empty list on other exceptions

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
