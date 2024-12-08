from src.service.controller_service.crawl_controller import CrawlController
from src.service.controller_service.transformation_controller import TransformationController



transformation_controller = TransformationController()


def crawl_data():
    # 6. Crawl_Data:
    # 6.1. sử hàm getConfig của crawlController đã tạo trước đó
    crawl_controller.get_config()


def insert_new_log_crawler_daily():
    crawl_controller.call_controller_procedure(insert_new_log_crawler_daily_procedure, ())




# Hàm này dùng để transform data và load data vào warehouse
# Hiện thực code ở thư mục src/service/transform_service
def transforms_data():
    # Lấy cấu từ controller
    transformation_controller.get_config()
    pass


# Hàm này dùng để load data từ staging vào warehouse
# Hiện thực code ở thư mục src/service/load_data_warehourse_service
def load_data_from_staging_to_warehouse():
    # Lấy cấu từ controller
    # crawl_controller.call_staging_procedure('load_data_from_staging_to_warehouse', ())
    pass


# Hàm này dùng để load data từ warehouse vào data mart
# Hiện thực code ở thư mục src/service/aggregate_service
def load_data_from_warehouse_to_data_mart():
    # Lấy cấu từ controller
    # crawl_controller.call_staging_procedure('load_data_from_warehouse_to_data_mart', ())
    pass
