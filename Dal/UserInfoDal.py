
from typing import Optional
from Dal.MySQLHelper import MySQLHelper
from Model.UserInfoModel import UserInfoModel
from typing import List

class UserInfoDal:
    def add(self, user=UserInfoModel):
        query = """
        INSERT INTO UserInfo(DevSN, PIN, UserName, Passwd, IDCard, Grp, TZ, Pri)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user.DevSN, 
            user.PIN,
            user.UserName, 
            user.Passwd, 
            user.IDCard,
            user.Grp, 
            user.TZ, 
            user.Pri
        )
        return MySQLHelper.execute_non_query(query, params)

    def update(self, user=UserInfoModel):
        query = """
        UPDATE UserInfo SET 
            DevSN=%s, UserName=%s, Passwd=%s, IDCard=%s,
            Grp=%s, TZ=%s, Pri=%s 
        WHERE PIN=%s
        """
        params = (
            user.DevSN, 
            user.UserName, 
            user.Passwd, 
            user.IDCard,
            user.Grp, 
            user.TZ, 
            user.Pri, 
            user.PIN)
        return MySQLHelper.execute_non_query(query, params)

    def get(self, pin: str):
        query = "SELECT * FROM UserInfo WHERE PIN=%s"
        params = (pin,)
        result = MySQLHelper.execute_query(query, params)
        return result[0] if result else None

    def get_multiple(self, pins: List[str]):
        formatted_pins = ','.join(['%s'] * len(pins))
        query = f"SELECT * FROM UserInfo WHERE PIN IN ({formatted_pins})"
        params = tuple(pins)
        return MySQLHelper.execute_query(query, params)

    def get_all(self):
        query = """
        SELECT u.*,
            IFNULL(fp.FP9Count, 0) as FP9Count,
            IFNULL(fp.FP10Count, 0) as FP10Count,
            IFNULL(fp.FP12Count, 0) as FP12Count,
            IFNULL(bd.PalmCount, 0) as PalmCount,
            IFNULL(f.FaceCount, 0) + IFNULL(bp.BioPhotoCount, 0) as FaceCount
        FROM UserInfo u
        LEFT JOIN (
            SELECT PIN,
                SUM(CASE WHEN MajorVer = '9' THEN 1 ELSE 0 END) as FP9Count,
                SUM(CASE WHEN MajorVer = '10' THEN 1 ELSE 0 END) as FP10Count,
                SUM(CASE WHEN MajorVer = '12' THEN 1 ELSE 0 END) as FP12Count
            FROM TmpFP GROUP BY PIN
        ) fp ON u.PIN = fp.PIN
        LEFT JOIN (SELECT PIN, COUNT(ID) as FaceCount FROM TmpFace GROUP BY PIN) f ON u.PIN = f.PIN
        LEFT JOIN (
            SELECT PIN, COUNT(ID) as BioPhotoCount 
            FROM TmpBioPhoto WHERE type = '9' OR type = '0' GROUP BY PIN
        ) bp ON u.PIN = bp.PIN
        LEFT JOIN (
            SELECT PIN, COUNT(ID) as PalmCount 
            FROM TmpBioData WHERE type = '8' GROUP BY PIN
        ) bd ON u.PIN = bd.PIN
        ORDER BY u.PIN
        """
        return MySQLHelper.execute_query(query)

    def delete(self, pins: List[str]):
        formatted_pins = ','.join(['%s'] * len(pins))
        query = f"DELETE FROM UserInfo WHERE PIN IN ({formatted_pins})"
        params = tuple(pins)
        return MySQLHelper.execute_non_query(query, params)

    def clear_all(self):
        query = "DELETE FROM UserInfo"
        return MySQLHelper.execute_non_query(query)