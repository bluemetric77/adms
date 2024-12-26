import mysql.connector
from datetime import datetime
from typing import List
from Model.DeviceCmdModel import DeviceCmdModel
from Dal.MySQLHelper import MySQLHelper

MAX_BUFFER_CMD = 2 * 1024 * 1024  # 2MB buffer

class DeviceCmdDal:
    
    def add(self, dCmd:DeviceCmdModel):
        sql = """
        INSERT INTO DeviceCmds(
            DevSN, Content, CommitTime, TransTime, ResponseTime, ReturnValue
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (
            dCmd.DevSN,
            dCmd.Content,
            dCmd.CommitTime,
            None,  # TransTime is initially None
            None,  # ResponseTime is initially None
            dCmd.ReturnValue
        )
        
        return MySQLHelper.execute_non_query(sql, params)
    
    def send(self, dev_sn):
        sql = """
        SELECT ID, DevSN, Content, CommitTime, TransTime, ResponseTime, ReturnValue
        FROM DeviceCmds
        WHERE DevSN = %s AND (ReturnValue IS NULL OR LENGTH(ReturnValue) = 0)
        LIMIT 200
        """
        
        params = (dev_sn,)
        dt_cmd = MySQLHelper.execute_query(sql, params)
        
        if not dt_cmd:
            return "OK"
        
        sb_cmd = []
        sb_cmd_id = []
        
        for row in dt_cmd:
            curr_cmd = f"C:{row['ID']}:{row['Content']}\n"
            curr_cmd_len = len(curr_cmd.encode('utf-8'))
            str_orders_len = len(''.join(sb_cmd).encode('utf-8'))
            
            if curr_cmd_len + str_orders_len > MAX_BUFFER_CMD:
                break
            
            sb_cmd.append(curr_cmd)
            sb_cmd_id.append(str(row['ID']))
        
        ids = ','.join(sb_cmd_id)
        
        if ids:
            update_sql = f"UPDATE DeviceCmds SET TransTime = %s WHERE ID IN ({ids})"
            MySQLHelper.execute_non_query(update_sql, (self._get_current_datetime(),))
        
        return ''.join(sb_cmd) if sb_cmd else "OK"
    
    def get_by_time(self, start_time, end_time, dev_sn):
        where_dev_sn = f" AND DevSN = %s " if dev_sn else ""
        sql = f"""
        SELECT * FROM DeviceCmds
        WHERE CommitTime > %s AND CommitTime < %s
        {where_dev_sn}
        ORDER BY CommitTime DESC
        """
        
        params = (start_time, end_time)
        if dev_sn:
            params += (dev_sn,)
        
        return MySQLHelper.execute_non_query(sql, params)
        
    def get_all(self):
        sql = "SELECT * FROM DeviceCmds ORDER BY CommitTime DESC"
        return MySQLHelper.execute_query(sql)
    
    def update(self, arr_content):
        sql = """
        UPDATE DeviceCmds SET
            ResponseTime = %s,
            ReturnValue = %s
        WHERE ID = %s
        """
        
        many_sql = []
        content_list = arr_content.split('\n')
        
        for content in content_list:
            if content:
                content_parts = content.split('&')
                cmd_id = content_parts[0].split('=')[1]
                return_value = content
                params = (
                    self._get_current_datetime(),
                    return_value,
                    cmd_id
                )
                many_sql.append((sql, params))
        MySQLHelper.execute_transaction(many_sql)
    
    def delete(self, list_id):
        ids = ','.join([str(id) for id in list_id])
        sql = f"DELETE FROM DeviceCmds WHERE ID IN ({ids})"
        return MySQLHelper.execute_non_query(sql)
    
    def clear_all(self):
        sql = "DELETE FROM DeviceCmds"
        return MySQLHelper.execute_non_query(sql)
    
    def _get_current_datetime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')