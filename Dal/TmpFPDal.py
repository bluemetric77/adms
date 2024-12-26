from typing import List
from Model.TmpFPModel import TmpFPModel 
from Dal.MySQLHelper import MySQLHelper # Assuming TmpFPModel is defined elsewhere

class TmpFPDal:
    def __init__(self):
        pass

    def get(self, pin: str) -> List[TmpFPModel]:
        sql = """
        SELECT * FROM TmpFP WHERE Pin = %s;
        """
        params = (pin,)
        result = MySQLHelper.execute_query(sql, params)

        if not result:
            return []

        fps = []
        for row in result:
            fp = TmpFPModel()
            fp.ID = int(row['ID'])
            fp.Pin = row['Pin']
            fp.Fid = row['Fid']
            fp.Size = int(row['Size'])
            fp.Valid = row['Valid']
            fp.Tmp = row['Tmp']
            fp.MajorVer = row['MajorVer']
            fp.MinorVer = row['MinorVer']
            fp.Duress = row['Duress']
            fps.append(fp)
        return fps

    def get_count(self, pin: str, ver: str) -> int:
        sql = """
        SELECT COUNT(*) FROM TmpFP
        WHERE Pin = %s AND MajorVer = %s;
        """
        params = (pin.lower(), ver.lower())
        return MySQLHelper.execute_scalar(sql, params)

    def add(self, model: TmpFPModel) -> int:
        sql = """
        DELETE FROM TmpFP WHERE Pin = %s AND MajorVer = %s AND Fid = %s;"""
        MySQLHelper.execute_non_query(sql, (model.Pin,model.MajorVer,model.Fid))

        sql = """
        INSERT INTO TmpFP (Pin, Fid, Size, Valid, Tmp, MajorVer, MinorVer, Duress)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            model.Pin,
            model.Fid,
            model.Size,
            model.Valid,
            model.Tmp,
            model.MajorVer,
            model.MinorVer,
            model.Duress
        )
        return MySQLHelper.execute_non_query(sql, params)

    def delete(self, pins: List[str]) -> int:
        sql = f"""
        DELETE FROM TmpFP WHERE Pin IN ({','.join(['%s'] * len(pins))});
        """
        return MySQLHelper.execute_non_query(sql, pins)

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpFP"
        return MySQLHelper.execute_non_query(sql)
