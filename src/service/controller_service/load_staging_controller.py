import mysql.connector

from src.config.database import staging_connector
from src.config.procedure import get_log_load_staging, get_script_load_file_by_source
from src.service.controller_service.database_controller import Controller


class LoadStagingController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        # 10.2 Gọi hàm call_procedure (4.1) để lấy cấu hình cho load staging
        data = self.call_controller_procedure(get_log_load_staging, ())

        # 10.3 kiểm tra các thông số cấu hình lấy về data != None
        if data is None:
            # 10.3.1 Không lấy được cấu hình
            return
        print(data['name'])
        print(data['file_part'])
        # 10.3.2 Lấy được cấu hình
        # 10.4 Lấy đoạn script load file từ database
        script= self.call_controller_procedure(get_script_load_file_by_source, (data['name'], data['file_part']))
        print(script)
        connection = self.get_staging_connection()
        # commands = script.split(";")
        cursor: mysql.connector.connection.MySQLCursor = connection.cursor()
        cursor.execute("SET GLOBAL local_infile = 1;")
        # for command in commands:
        #     command = command.strip()
        #     if command:  # Bỏ qua lệnh rỗng
        #         print(f"Executing command: {command}")
        #         cursor.execute(command)
        script=script['load_file_script']
        script=script.replace("\\","")
        print(script)
        try:
            cursor.execute(script)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    import asyncio
    c = LoadStagingController()
    c.get_config()