from typing import List
from Model.TmpFveinModel import TmpFveinModel  
from Utils.Tools import Tools  
from Dal.MySQLHelper import MySQLHelper


class TmpFveinDal:
    def __init__(self):
        pass

    def get(self, pins: List[str], ver: str) -> List[TmpFveinModel]:
        sql = """
        SELECT * FROM TmpFvein WHERE Pin IN (%s) AND Ver = %s;
        """
        params = (",".join(["%s"] * len(pins)), ver)
        result = MySQLHelper.execute_query(sql % params[0], tuple(pins))

        if not result:
            return []

        fvein_list = []
        for row in result:
            fvein = TmpFveinModel()
            fvein.ID = int(row['ID'])
            fvein.Pin = row['Pin']
            fvein.Fid = row['Fid']
            fvein.Index = row['Index']
            fvein.Size = int(row['Size'])
            fvein.Valid = row['Valid']
            fvein.Tmp = row['Tmp']
            fvein.Ver = row['Ver']
            fvein.Duress = row['Duress']
            fvein_list.append(fvein)

        return fvein_list

    def get_count(self, pin: str, ver: str) -> int:
        sql = """
        SELECT COUNT(*) FROM TmpFvein WHERE Pin = %s AND Ver = %s;
        """
        params = (pin.lower(), ver.lower())
        result = MySQLHelper.execute_scalar(sql, params)
        return int(result) if result else 0

    def add(self, model: TmpFveinModel) -> int:
        sql = """
        DELETE FROM TmpFvein WHERE Pin = %s AND Ver = %s AND Fid = %s AND Index = %s;
        INSERT INTO TmpFvein (Pin, Fid, Index, Size, Valid, Tmp, Ver, Duress)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            model.Pin, model.Ver, model.Fid, model.Index,
            model.Pin, model.Fid, model.Index, model.Size,
            model.Valid, model.Tmp, model.Ver, model.Duress
        )
        return MySQLHelper.execute_non_query(sql, params)

    def delete(self, pins: List[str]) -> int:
        sql = """
        DELETE FROM TmpFvein WHERE Pin IN (%s);
        """
        params = (",".join(["%s"] * len(pins)),)
        result = MySQLHelper.execute_non_query(sql % params[0], tuple(pins))
        return result

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpFvein"
        return MySQLHelper.execute_non_query(sql)
