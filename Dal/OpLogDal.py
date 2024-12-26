from datetime import datetime
from typing import List, Dict, Optional
from Dal.MySQLHelper import MySQLHelper
from Model.OpLogModel import OpLogModel

class OpLogDal:
    def get(self) -> List[Dict]:
        """Get all operation logs."""
        sql = "SELECT * FROM OpLog ORDER BY OpTime DESC"
        return MySQLHelper.execute_query(sql)
    
    def get_all(self) -> List[Dict]:
        """Get all operation logs."""
        sql = "SELECT * FROM OpLog ORDER BY OpTime DESC"
        return MySQLHelper.execute_query(sql)

    def get_oplog_by_time(self, start_time: datetime, end_time: datetime, dev_sn: Optional[str] = "") -> List[Dict]:
        """Get operation logs filtered by time and device serial number."""
        where_dev_sn = f" AND DeviceID='{dev_sn}'" if dev_sn else ""
        
        sql = f"""
        SELECT * FROM OpLog
        WHERE OpTime > %s AND OpTime < %s
        {where_dev_sn}
        ORDER BY OpTime DESC
        """
        
        params = (start_time, end_time)
        return MySQLHelper.execute_query(sql, params)
    
    def clear_all(self) -> int:
        """Clear all operation logs."""
        sql = "DELETE FROM OpLog"
        return MySQLHelper.execute_non_query(sql)
    
    def add(self, oplog: OpLogModel) -> int:
        """Add a new operation log."""
        sql = """
        INSERT INTO OpLog(Operator, OpTime, OpType, User, Obj1, Obj2, Obj3, Obj4, DeviceID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            oplog.Operator,
            oplog.OpTime,
            oplog.OpType,
            oplog.User,
            oplog.Obj1,
            oplog.Obj2,
            oplog.Obj3,
            oplog.Obj4,
            oplog.DeviceID
        )
        
        return MySQLHelper.execute_non_query(sql, params)