from typing import Optional, List, Dict
from datetime import datetime
from Dal.MySQLHelper import MySQLHelper
from Model.SMSModel import SMSModel

class SMSDal:
    def get_all(self, sql_where: Optional[str] = "") -> List[Dict]:
        where_clause = f"WHERE {sql_where}" if sql_where else ""
        
        sql = f"""
        SELECT ID, SMSId, Type, ValidTime, BeginTime, UserID, Content,
               CASE Type
                    WHEN 253 THEN 'Common'
                    WHEN 254 THEN 'User'
                    WHEN 255 THEN 'Reserved'
                    ELSE '' END AS TypeName
        FROM SMS
        {where_clause}
        """
        return MySQLHelper.execute_query(sql)

    def get(self, sms_id: str) -> Optional[Dict]:
        sql_where = f"SMSId='{sms_id}'"
        result = self.get_all(sql_where)
        return result[0] if result else None
    
    def add(self, model: Dict) -> int:
        sql = """
        INSERT INTO SMS (SMSId, Type, ValidTime, BeginTime, UserID, Content)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            model['SMSId'],
            model['Type'],
            model['ValidTime'],
            model['BeginTime'],
            model['UserID'],
            model['Content']
        )
        return MySQLHelper.execute_non_query(sql, params)
    
    def delete(self, sms_id: str) -> int:
        sql = "DELETE FROM SMS WHERE SMSId=%s"
        return MySQLHelper.execute_non_query(sql, (sms_id,))
    
    def update(self, model: Dict) -> int:
        sql = """
        UPDATE SMS
        SET SMSId=%s, Type=%s, ValidTime=%s, BeginTime=%s, UserID=%s, Content=%s
        WHERE ID=%s
        """
        params = (
            model['SMSId'],
            model['Type'],
            model['ValidTime'],
            model['BeginTime'],
            model['UserID'],
            model['Content'],
            model['ID']
        )
        return MySQLHelper.execute_non_query(sql, params)
    
    def clear_all(self) -> int:
        sql = "DELETE FROM SMS"
        return MySQLHelper.execute_non_query(sql)
