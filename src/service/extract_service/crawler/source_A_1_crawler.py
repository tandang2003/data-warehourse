from datetime import datetime

from selenium.common import WebDriverException, NoSuchElementException

from src.config.setting import SOURCE_A_1, SOURCE_A_BASE
from src.service.extract_service.crawler.config_crawler import config_crawler_source_A_1
from src.service.extract_service.crawler.paging_base_crawler import PagingBase
from src.util.file_util import write_json_to_csv, write_json_to_file
from selenium.webdriver.common.by import By


class SourceA1Crawler(PagingBase):
    _base_url = SOURCE_A_1
    _domain = SOURCE_A_BASE

    def crawl_page(self, page):
        url_page = f"{self._base_url}/p{page}"
        print(f"Visiting page: {url_page}")
        self.get_url(url_page)

        # Wait for 5 seconds
        self.wait(5)
        driver = self.driver.page_source
        self.filter_script(driver)

        estate_list = self.soup.select(".js__card")
        list_url = []
        for (estate) in estate_list:
            link = estate.select_one(".js__product-link-for-product-id").get("href")
            if link.startswith("https://"):
                continue
            else:
                list_url.append(f"{self._domain}{str(link)}")
        return list_url

    def crawl_item(self, url):
        try:
            self.get_url(url)
        except WebDriverException as e:
            return None
        print(f"Visiting item: {url}")

        self.wait(10)
        current_url = self.driver.current_url
        if current_url != url:
            return None

        driver = self.driver.page_source
        self.filter_script(driver)

        xpath_subject = self.find_elements_with_xpath("//*[contains(@class, 'pr-title')]")
        subject = xpath_subject[0].text.strip() if xpath_subject else None

        xpath_area = self.find_elements_with_xpath(
            "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Diện tích']/following-sibling::*[1]")
        area = xpath_area[0].text.strip() if xpath_area else None

        xpath_address = self.find_elements_with_xpath("//*[contains(@class, 'js__pr-address')]")
        address = xpath_address[0].text.strip() if xpath_address else None

        xpath_price = self.find_elements_with_xpath(
            "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Mức giá']/following-sibling::*[1]")
        price = xpath_price[0].text if xpath_price else None

        xpath_description = self.find_elements_with_xpath("//*[contains(@class, 're__detail-content')]")
        description = xpath_description[0].text if xpath_description else None

        xpath_images = self.find_elements_with_xpath("//*[contains(@class, 'slick-track')]//img")
        images = list(map(lambda img: img.get_attribute('src'), xpath_images)) if xpath_images else None

        xpath_natural_key = self.find_elements_with_xpath("//*[@id='product-detail-web']")
        natural_key = xpath_natural_key[0].get_attribute("prid").strip() if xpath_natural_key else None

        xpath_oriented = self.find_elements_with_xpath(
            "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Hướng nhà']/following-sibling::*[1]")
        orientation = xpath_oriented[0].text.strip() if xpath_oriented else None

        xpath_bathroom = self.find_elements_with_xpath(
            "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số toilet']/following-sibling::*[1]")
        bathroom = xpath_bathroom[0].text.strip() if xpath_bathroom else None

        xpath_bedroom = self.find_elements_with_xpath(
            "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số phòng ngủ']/following-sibling::*[1]")
        bedroom = xpath_bedroom[0].text.strip() if xpath_bedroom else None

        xpath_legal = self.find_elements_with_xpath(
            "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Pháp lý']/following-sibling::*[1]")
        legal = xpath_legal[0].text.strip() if xpath_legal else None

        xpath_email = self.find_elements_with_xpath("//*[@id='email']")
        email = xpath_email[0].get_attribute("data-email") if xpath_email else None

        xpath_fullname = self.find_elements_with_xpath("(//*[contains(@class, 'js_contact-name')])[1]")
        fullname = xpath_fullname[0].get_attribute("title") if xpath_fullname else None

        created_at = datetime.now().strftime("%d/%m/%Y")

        xpath_start_date = self.find_elements_with_xpath(
            "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày đăng']/following-sibling::*[1]")
        start_date = xpath_start_date[0].text if xpath_start_date else None
        xpath_end_date = self.find_elements_with_xpath(
            "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày hết hạn']/following-sibling::*[1]")

        end_date = xpath_end_date[0].text.strip() if xpath_end_date else None
        src = current_url

        result = {
            "subject": subject,
            "address": address,
            "description": description,
            "price": price,
            "images": images,
            "area": area,
            "orientation": orientation,
            "bathroom": bathroom,
            "bedroom": bedroom,
            "legal": legal,
            "fullname": fullname,
            "email": email,
            "created_at": created_at,
            "start_date": start_date,
            "end_date": end_date,
            "src": src,
            "natural_key": natural_key
        }

        # Loop through each property in the config
        for field_name, properties in config_crawler_source_A_1.items():
            print(f"Field Name: {field_name}")  # Print the name of the field
            for prop_name, prop_value in properties.items():
                print(f"  {prop_name}: {prop_value}")

        return result

    def after_run(self):
        data = self._list_item
        current_date = datetime.now().strftime("%Y_%m_%d__%H_%M")
        print("data: ")
        print(data)
        write_json_to_file(f"source_1_{current_date}.json", data)
        filename = f"source_1_{current_date}.csv"
        write_json_to_csv(filename, data)
        print(f"Data has been saved to {filename}")

    def handle_error_item(self, error):
        super().handle_error_item(error)

    @property
    def base_url(self):
        return self._base_url

    def find_elements_with_xpath(self, xpath):
        try:
            # Attempt to find elements using the provided XPath
            elements = self.driver.find_elements(By.XPATH, xpath)

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
        method = field_properties.get("method", None)
        selector = field_properties.get("selector", None)
        attribute = field_properties.get("attribute", None)
        quantity = field_properties.get("quantity")
        xpath = self.find_elements_with_xpath(selector)

        if quantity is None:
            return list(map(lambda img: img.get_attribute('attribute'), xpath)) if xpath else None
        if method == "time":
            return datetime.now().strftime("%d/%m/%Y")
        if method == "url":
            return self.driver.current_url
        if method == "description":
            return xpath[quantity].text if xpath else None
        if method == "get_attribute":
            return xpath[quantity].get_attribute(attribute) if xpath else None
        if method == "text":
            return xpath[quantity].text.strip() if xpath else None
        return None