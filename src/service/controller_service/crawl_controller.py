from src.config.procedure import procedure_get_log_crawler_config
from src.service.controller_service.database_controller import Controller


class CrawlController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        data = self.call_controller_procedure(procedure_get_log_crawler_config, ())
        print(data)
        # return self.call_staging_procedure("GetConfigById", (1,))
if __name__ == '__main__':
    c= CrawlController()
    c.get_config()