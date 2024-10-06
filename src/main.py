from src.config import DRIVER_PATH
from src.crawler.source_1_crawler import Source1Crawler
from src.util import write_json_to_file


def run_crawlers():
    # Initialize Source1Crawler
    source1_crawler = Source1Crawler(driver_path=DRIVER_PATH)
    source1_crawler.setup_driver(headless=True)  # Headless browser option
    data = source1_crawler.crawl()
    write_json_to_file("source_1.json", data)


if __name__ == "__main__":
    run_crawlers()
