import mysql.connector

from src.config.procedure import get_script_load_file_by_source
from src.service.controller_service.database_controller import Controller


class LoadStagingController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        # 10.2 Gọi hàm call_procedure (4.1) để lấy cấu hình cho load staging
        # data = self.call_controller_procedure(get_log_load_staging, ())
        #
        # # 10.3 kiểm tra các thông số cấu hình lấy về data != None
        # if data is None:
        #     # 10.3.1 Không lấy được cấu hình
        #     return
        # print(data['name'])
        # print(data['file_part'])

        data = {
            'name': 'batdongsan.com.vn',
            'file_part': 'D:/university/data_warehouse/sql/data/batdongsan_com_vn_data.csv'
        }
        # 10.3.2 Lấy được cấu hình
        # 10.4 Lấy đoạn script load file từ database
        sql_list = self.call_controller_procedure(get_script_load_file_by_source, (data['name'], data['file_part']))
        connection = self.get_staging_connection()
        cursor: mysql.connector.connection.MySQLCursor = connection.cursor()
        print(sql_list)
        try:
            for sql in sql_list:
                step = sql['step']
                sql_statement = sql['sql_statement']
                print(f"Executing step: {step}")
                cursor.execute(sql_statement)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    c = LoadStagingController()
    c.get_config()