from typing import Optional
from Dal.MySQLHelper import MySQLHelper
from typing import List

class WorkCodeDal:
    def add(self, work_code):
        sql = "INSERT INTO WorkCode (workcode, workname) VALUES (%s, %s)"
        params = (work_code['workcode'], work_code['workname'])
        return MySQLHelper.execute_query(sql, params)

    def delete(self, work_code):
        sql = "DELETE FROM WorkCode WHERE workcode = %s"
        params = (work_code,)
        return MySQLHelper.execute_query(sql, params)

    def update(self, work_code):
        sql = """
            UPDATE WorkCode 
            SET workcode = %s, workname = %s 
            WHERE id = %s
        """
        params = (work_code['workcode'], work_code['workname'], work_code['id'])
        return MySQLHelper.execute_query(sql, params)

    def get_by_work_code(self, work_code):
        sql = "SELECT * FROM WorkCode WHERE workcode = %s"
        params = (work_code,)
        result = MySQLHelper.fetch_query(sql, params)
        if result:
            return result[0]  # Return the first matching row
        return None

    def get_all(self):
        sql = "SELECT * FROM WorkCode"
        return MySQLHelper.fetch_query(sql)