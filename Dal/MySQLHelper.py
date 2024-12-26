import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Tuple, Union


class MySQLHelper:
    # Update with your MySQL connection details
    HOST = "localhost"
    USER = "root"
    PASSWORD = "admin"
    DATABASE = "dbkbu"
    PORT = 3306

    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=MySQLHelper.HOST,
                user=MySQLHelper.USER,
                password=MySQLHelper.PASSWORD,
                database=MySQLHelper.DATABASE,
                port=MySQLHelper.PORT,
                charset='utf8mb4',
                collation='utf8mb4_general_ci'                
            )
            #print("Connection to the database was successful.")
            return connection
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    @staticmethod
    def execute_non_query(sql: str, params: Optional[Union[Tuple, List]] = None, pmsg=False) -> int:
        try:
            conn = MySQLHelper.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            rows_affected = cursor.rowcount
            if pmsg:
                if rows_affected != -1:
                    print(f"Successfully {rows_affected} row(s) affected")
                else:
                    print("Failed to insert record.")   

            return rows_affected
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return  None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def execute_scalar(sql: str, params: Optional[Union[Tuple, List]] = None) -> Optional[Union[int, str, float]]:
        try:
            conn = MySQLHelper.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return  None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def execute_query(sql: str, params: Optional[Union[Tuple, List]] = None) -> List[dict]:
        try:
            conn = MySQLHelper.get_connection()
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows= cursor.fetchall()
            return rows if rows else None
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return  None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def execute_transaction(sql_commands: List[Tuple[str, Optional[Union[Tuple, List]]]]) -> None:
        try:
            conn = MySQLHelper.get_connection()
            cursor = conn.cursor()
            for sql, params in sql_commands:
                cursor.execute(sql, params)
            conn.commit()
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error executing SQL: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_data_table(sql: str, params: Optional[Union[Tuple, List]] = None) -> List[dict]:
        return MySQLHelper.execute_query(sql, params)

