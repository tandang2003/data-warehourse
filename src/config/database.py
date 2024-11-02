import mysql.connector
from mysql.connector import Error, pooling

from src.config.setting import CONTROLLER_DB_HOST, CONTROLLER_DB_PORT, CONTROLLER_DB_NAME, CONTROLLER_DB_USER, \
    CONTROLLER_DB_PASS, CONTROLLER_DB_POOL_NAME, CONTROLLER_DB_POOL_SIZE


class _MySQLCRUD:
    def __init__(self, host, port, user, password, database, pool_name, pool_size=5):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,  # Resets session on each connection reuse
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            print(f"Connection pool created with pool size: {pool_size}")
        except Error as e:
            print(f"Error creating connection pool: {e}")
            self.pool = None

    def get_connection(self):
        """Get a connection from the pool."""
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Failed to get connection from pool: {e}")
            return None

    def create(self, table=None, data=None, custom_query=None):
        """Create a new record in the database."""
        connection = self.get_connection()
        if connection is None:
            return
        try:
            cursor = connection.cursor()
            if custom_query:
                cursor.execute(custom_query, data)
            else:
                query = f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join(['%s'] * len(data))})"
                cursor.execute(query, tuple(data.values()))
            connection.commit()
            print("Record inserted successfully.")
        except Error as e:
            print(f"Failed to insert record into database: {e}")
        finally:
            cursor.close()
            connection.close()

    def read(self, table=None, condition=None, columns="*", custom_query=None, params=None):
        """Read data from the database."""
        connection = self.get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor()
            if custom_query:
                cursor.execute(custom_query, params)
            else:
                query = f"SELECT {columns} FROM {table}"
                if condition:
                    query += f" WHERE {condition}"
                cursor.execute(query, params if params else ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Failed to read from database: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    def update(self, table=None, data=None, condition=None, custom_query=None):
        """Update a record in the database."""
        connection = self.get_connection()
        if connection is None:
            return
        try:
            cursor = connection.cursor()
            if custom_query:
                cursor.execute(custom_query, data)
            else:
                set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
                query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
                cursor.execute(query, tuple(data.values()))
            connection.commit()
            print("Record updated successfully.")
        except Error as e:
            print(f"Failed to update record in the database: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete(self, table=None, condition=None, custom_query=None, params=None):
        """Delete a record from the database."""
        connection = self.get_connection()
        if connection is None:
            return
        try:
            cursor = connection.cursor()
            if custom_query:
                cursor.execute(custom_query, params)
            else:
                query = f"DELETE FROM {table} WHERE {condition}"
                cursor.execute(query, params if params else ())
            connection.commit()
            print("Record deleted successfully.")
        except Error as e:
            print(f"Failed to delete record from database: {e}")
        finally:
            cursor.close()
            connection.close()

    def close_pool(self):
        """Close the pool and all connections."""
        try:
            self.pool.close()
            print("Connection pool closed.")
        except Error as e:
            print(f"Error closing the connection pool: {e}")


controller_connector = _MySQLCRUD(
    host=CONTROLLER_DB_HOST,
    port=CONTROLLER_DB_PORT,
    database=CONTROLLER_DB_NAME,
    user=CONTROLLER_DB_USER,
    password=CONTROLLER_DB_PASS,
    pool_name=CONTROLLER_DB_POOL_NAME,
    pool_size=CONTROLLER_DB_POOL_SIZE
)

staging_connector= None
warehouse_connector = None

