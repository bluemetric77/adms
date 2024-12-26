from Utils.Tools import Tools
from Dal.MySQLHelper import MySQLHelper
from Model.DeviceModel import DeviceModel
from datetime import datetime

class DeviceDal:
    def try_convert_to_int32(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def get_all(self, sql_where: str):
        sql_where = f"WHERE {sql_where}" if sql_where else ""
        sql = f"SELECT * FROM Device {sql_where};"
        return MySQLHelper.execute_query(sql)

    def get(self, devSN: str):
        sql_where = f"DevSN='{devSN}'"
        result = self.get_all(sql_where)
        if not result:
            return None

        dt = result[0]
        device = DeviceModel()
        
        device.ID = self.try_convert_to_int32(dt.get("ID"))
        device.DevSN = str(dt.get("DevSN", ""))
        device.TransInterval = str(dt.get("TransInterval", ""))
        device.TransTimes = str(dt.get("TransTimes", ""))
        device.Encrypt = str(dt.get("Encrypt", ""))
        
        # Convert to datetime if the value exists
        last_request_time_str = str(dt.get("LastRequestTime", ""))
        if last_request_time_str=='None':
            device.LastRequestTime = None
        elif last_request_time_str:
            if isinstance(last_request_time_str, bytes):
                last_request_time_str = last_request_time_str.decode('utf-8')
            try:
                device.LastRequestTime = datetime.strptime(last_request_time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                device.LastRequestTime = None
        else:
            device.LastRequestTime = None
            
        device.DevIP = str(dt.get("DevIP", ""))
        device.DevMac = str(dt.get("DevMac", ""))
        device.DevFirmwareVersion = str(dt.get("DevFirmwareVersion", ""))
        
        device.UserCount = self.try_convert_to_int32(dt.get("UserCount"))
        device.AttCount = self.try_convert_to_int32(dt.get("AttCount"))
        
        device.DevName = str(dt.get("DevName", ""))
        device.TimeZone = str(dt.get("TimeZone", ""))
        device.Timeout = self.try_convert_to_int32(dt.get("Timeout"))
        device.SyncTime = self.try_convert_to_int32(dt.get("SyncTime"))
        
        device.AttLogStamp = str(dt.get("ATTLOGStamp", ""))
        device.OperLogStamp = str(dt.get("OPERLOGStamp", ""))
        device.AttPhotoStamp = str(dt.get("ATTPHOTOStamp", ""))
        device.ErrorDelay = str(dt.get("ErrorDelay", ""))
        device.Delay = str(dt.get("Delay", ""))
        device.TransFlag = str(dt.get("TransFlag", ""))
        device.Realtime = str(dt.get("Realtime", ""))
        device.VendorName = str(dt.get("VendorName", ""))
        device.IRTempDetectionFunOn = str(dt.get("IRTempDetectionFunOn", ""))
        device.MaskDetectionFunOn = str(dt.get("MaskDetectionFunOn", ""))
        
        device.MultiBioDataSupport = str(dt.get("MultiBioDataSupport", ""))
        device.MultiBioPhotoSupport = str(dt.get("MultiBioPhotoSupport", ""))
        device.MultiBioVersion = str(dt.get("MultiBioVersion", ""))
        device.MultiBioCount = str(dt.get("MultiBioCount", ""))
        device.MaxMultiBioDataCount = str(dt.get("MaxMultiBioDataCount", ""))
        device.MaxMultiBioPhotoCount = str(dt.get("MaxMultiBioPhotoCount", ""))
        return device

    def add(self, device: DeviceModel):
        sql = """
        INSERT INTO Device (
            DevSN, TransInterval, TransTimes, Encrypt, LastRequestTime, DevIP, DevMac, DevFirmwareVersion,
            UserCount, AttCount, DevName, TimeZone, Timeout, SyncTime, ATTLOGStamp, OPERLOGStamp, ATTPHOTOStamp,
            ErrorDelay, Delay, TransFlag, Realtime, VendorName, IRTempDetectionFunOn, MaskDetectionFunOn
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            device.DevSN, device.TransInterval, device.TransTimes, device.Encrypt, device.LastRequestTime,
            device.DevIP, device.DevMac, device.DevFirmwareVersion, device.UserCount, device.AttCount,
            device.DevName, device.TimeZone, device.Timeout, device.SyncTime, device.AttLogStamp, device.OperLogStamp,
            device.AttPhotoStamp, device.ErrorDelay, device.Delay, device.TransFlag, device.Realtime,
            device.VendorName, device.IRTempDetectionFunOn, device.MaskDetectionFunOn
        )
        MySQLHelper.execute_non_query(sql, params)

    def delete(self, devSN: str):
        sql = "DELETE FROM Device WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (devSN,))

    def update(self, device: DeviceModel):
        sql = """
        UPDATE Device SET 
            TransInterval=%s, TransTimes=%s, Encrypt=%s, LastRequestTime=%s, DevIP=%s, DevMac=%s, DevFirmwareVersion=%s,
            UserCount=%s, AttCount=%s, DevName=%s, TimeZone=%s, Timeout=%s, SyncTime=%s, ATTLOGStamp=%s, OPERLOGStamp=%s,
            ATTPHOTOStamp=%s, ErrorDelay=%s, Delay=%s, TransFlag=%s, Realtime=%s, VendorName=%s, IRTempDetectionFunOn=%s,
            MaskDetectionFunOn=%s, MultiBioDataSupport=%s, MultiBioPhotoSupport=%s, MultiBioVersion=%s, MultiBioCount=%s,
            MaxMultiBioDataCount=%s, MaxMultiBioPhotoCount=%s 
        WHERE DevSN=%s
        """
        params = (
            device.TransInterval, device.TransTimes, device.Encrypt, device.LastRequestTime, device.DevIP, 
            device.DevMac, device.DevFirmwareVersion, device.UserCount, device.AttCount, device.DevName, 
            device.TimeZone, device.Timeout, device.SyncTime, device.AttLogStamp, device.OperLogStamp, 
            device.AttPhotoStamp, device.ErrorDelay, device.Delay, device.TransFlag, device.Realtime, 
            device.VendorName, device.IRTempDetectionFunOn, device.MaskDetectionFunOn, device.MultiBioDataSupport, 
            device.MultiBioPhotoSupport, device.MultiBioVersion, device.MultiBioCount, device.MaxMultiBioDataCount, 
            device.MaxMultiBioPhotoCount, device.DevSN
        )
        MySQLHelper.execute_non_query(sql, params)

    def update_att_log_stamp(self, stamp: str, devSN: str):
        sql = "UPDATE Device SET ATTLOGStamp=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (stamp, devSN))

    def set_zero_att_log_stamp(self, list_dev_sn: list):
        sql = f"UPDATE Device SET ATTLOGStamp='0' WHERE DevSN IN ({', '.join(['%s' for _ in list_dev_sn])})"
        MySQLHelper.execute_non_query(sql, tuple(list_dev_sn))

    def update_oper_log_stamp(self, stamp: str, devSN: str):
        sql = "UPDATE Device SET OPERLOGStamp=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (stamp, devSN))

    def update_error_log_stamp(self, stamp: str, devSN: str):
        sql = "UPDATE Device SET ERRORLOGStamp=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (stamp, devSN))

    def update_att_photo_stamp(self, stamp: str, devSN: str):
        sql = "UPDATE Device SET ATTPHOTOStamp=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (stamp, devSN))

    def set_zero_stamp(self, list_dev_sn: list):
        sql = f"""
        UPDATE Device SET 
            OPERLOGStamp='0', ATTLOGStamp='0', ATTPHOTOStamp='0' 
        WHERE DevSN IN ({', '.join(['%s' for _ in list_dev_sn])})
        """
        MySQLHelper.execute_non_query(sql, tuple(list_dev_sn))

    def set_last_request_time(self, devSN: str):
        sql = "UPDATE Device SET LastRequestTime=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (Tools.get_datetime_now_string(), devSN))

    def update_vendor_name(self, sn: str, vendor_name: str):
        sql = "UPDATE Device SET VendorName=%s WHERE DevSN=%s"
        MySQLHelper.execute_non_query(sql, (vendor_name, sn))

    def get_all_dev_sn(self):
        sql = "SELECT DevSN FROM Device"
        result = MySQLHelper.execute_query(sql)
        return [row[0] for row in result]
