from src.config import SOURCE_A_URL
from src.crawler import BaseCrawler


class Source1Crawler(BaseCrawler):
    _base_url = "https://batdongsan.com.vn"

    def crawl(self):
        self.get_url(SOURCE_A_URL)

        # Wait for 5 seconds
        self.wait(5)

        driver = self.driver.page_source
        self.filter_script(driver)

        estate_list = self.soup.select(".js__card")
        id_link = {}
        for (estate) in estate_list:
            natural_id = estate.select_one(".js__product-link-for-product-id").get('data-product-id')
            link = estate.select_one(".js__product-link-for-product-id").get("href")
            id_link[natural_id] = str(self._base_url + link)

        items = []
        for (natural_id, link) in id_link.items():
            item = self.crawlItem(link)
            item["natural_id"] = natural_id
            item["src"] = link
            items.append(item)
        self.close()
        return items

    def crawlItem(self, url):
        self.get_url(url)
        button = self.driver.find_element_by_css_selector(".phoneEvent")
        button.click()

        print(f"Visiting {SOURCE_A_URL}")

        # Wait for 5 seconds
        self.wait(5)

        driver = self.driver.page_source
        self.filter_script(driver)

        title = self.soup.select_one(".pr-title").get_text(strip=True)
        address = self.soup.select_one(".js__pr-address").get_text(strip=True)
        description = self.soup.select_one(".re__detail-content").decode_contents()
        images = self.soup.select(".slick-track img")
        result = {
            "Subject": title,
            "Address": address,
            "Description": description
        }
        properties = self.soup.select(".re__pr-specs-content-item")
        result["properties"] = {}
        result["images"] = []
        for item in images:
            result["images"].append(item.get("src"))
        for item in properties:
            key = item.select_one(".re__pr-specs-content-item-title").get_text(strip=True)
            value = item.select_one(".re__pr-specs-content-item-value").get_text(strip=True)
            result["properties"][key] = value

        seller = self.soup.select_one(".js__ob-agent-info")
        result['agent'] = {
            'avatar': seller.select_one("a").get("href"),
            'fullname': seller.select_one("a").get_text(strip=True),
        }

        return result

# class Converter(IConverter):
#     def __init__(self, data):
#         self.data = data
#
#     def convert(self):
#         converted_data = []
#         for item in self.data:
#             converted_data.append({
#                 "Subject": item["Subject"],
#                 "Address": item["Address"],
#                 "Price": item["Price"],
#                 "Area": item["Area"],
#                 "Description": item["Description"]
#             })
#         return converted_data
