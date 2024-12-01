from src.config.procedure import get_log_crawler
from src.service.controller_service.database_controller import Controller
from src.service.extract_service.crawler.paging_base_crawler import PagingBase


class CrawlController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        data = self.call_controller_procedure(get_log_crawler, ())
        if data is None:
            return
        crawl = PagingBase(limit_page=data['limit_page'],
                           format_file=data['format_file'],
                           extension=data['file_extension'],
                           prefix=data['prefix'],
                           data_dir_path=data['data_dir_path'],
                           error_dir_path=data['error_dir_path'],
                           purpose=data['purpose'],
                           base_url=data['base_url'],
                           source_page=data['source_page'],
                           paging_pattern=data['paging_pattern'],
                           scenario=data['scenario'],
                           navigate_scenario=data['navigate_scenario'])
        result = crawl.handle()

        self.call_controller_procedure('insert_log_crawler', (
            data['id'],
            result['file'],
            result['error_file_name'],
            result['count_row'],
            result['status']))


if __name__ == '__main__':
    c = CrawlController()
    c.get_config()