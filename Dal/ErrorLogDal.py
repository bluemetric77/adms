from typing import List, Dict
from Dal.MySQLHelper import MySQLHelper
from Model.ErrorLogModel import ErrorLogModel

class ErrorLogDal:
    
    def add(self, model: ErrorLogModel):
        sql = """
        INSERT INTO ErrorLog(
            ErrorCode, ErrMsg, DataOrigin, CmdId, Additional, DeviceID
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (
            model.ErrCode,
            model.ErrMsg,
            model.DataOrigin,
            model.CmdId,
            model.Additional,
            model.DeviceID
        )
        
        return MySQLHelper.execute_non_query(sql, params)
    
    def get_all(self, dev_sn: str = None) -> List[Dict]:
        where_dev_sn = f" WHERE DeviceID = %s" if dev_sn else ""
        sql = f"""
        SELECT * FROM ErrorLog
        {where_dev_sn}
        ORDER BY id DESC
        """
        
        params = (dev_sn,) if dev_sn else ()
        return MySQLHelper.execute_query(sql, params)
    
    def clear_all(self) -> int:
        sql = "DELETE FROM ErrorLog"
        return MySQLHelper.execute_non_query(sql)
