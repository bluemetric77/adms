import mysql.connector
from datetime import datetime
from Dal.MySQLHelper import MySQLHelper
from Model.AttLogModel import AttLogModel


class AttLogDal:
    def get_by_time(self, start_time: datetime, end_time: datetime, user_id: str = "", dev_sn: str = ""):
        where_pin = f" AND a.PIN='{user_id}'" if user_id else ""
        where_dev_sn = f" AND DeviceID='{dev_sn}'" if dev_sn else ""
        
        sql = f"""
        SELECT a.*, w.workname 
        FROM AttLog a 
        LEFT JOIN WorkCode w ON a.workcode = w.workcode
        WHERE a.PIN <> '' 
        AND a.AttTime > %s 
        AND a.AttTime < %s
        {where_pin}
        {where_dev_sn}
        ORDER BY a.AttTime DESC
        """
        
        params = (start_time, end_time)
        return MySQLHelper.execute_query(sql,params)
    
    def get_all(self):
        sql = "SELECT * FROM AttLog ORDER BY AttTime DESC"
        return MySQLHelper.execute_query(sql)
    
    def clear_all(self):
        sql = "DELETE FROM AttLog"
        return MySQLHelper.execute_non_query(sql)
    
    def add(self, att_log=AttLogModel):
        sql = """
        INSERT INTO AttLog(
            PIN, AttTime, Status, Verify, WorkCode, Reserved1, Reserved2, MaskFlag, Temperature, DeviceID
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            att_log.PIN,
            att_log.AttTime,
            att_log.Status,
            att_log.Verify,
            att_log.WorkCode,
            att_log.Reserved1,
            att_log.Reserved2,
            att_log.MaskFlag,
            att_log.Temperature,
            att_log.DeviceID
        )
        return MySQLHelper.execute_non_query(sql, params)
    
    def is_exist(self, pin: str, att_time: datetime):
        sql = """
        SELECT COUNT(*)
        FROM AttLog 
        WHERE PIN = %s AND AttTime = %s
        """
        
        params = (pin, att_time)
        result = MySQLHelper.execute_scalar(sql, params)
        
        return result > 0
