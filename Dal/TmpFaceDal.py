from typing import List
from Model.TmpFaceModel import TmpFaceModel 
from Dal.MySQLHelper import MySQLHelper 

class TmpFaceDal:
    def __init__(self):
        pass

    def get(self, pin: str) -> List[TmpFaceModel]:
        sql = """
        SELECT * FROM TmpFace WHERE Pin = %s;
        """
        params = (pin,)
        result = MySQLHelper.execute_query(sql, params)

        if not result:
            return []

        face_list = []
        for row in result:
            face = TmpFaceModel()
            face.ID = int(row['ID'])
            face.Pin = row['Pin']
            face.Fid = row['Fid']
            face.Size = int(row['Size'])
            face.Valid = row['Valid']
            face.Tmp = row['Tmp']
            face.Ver = row['Ver']
            face_list.append(face)

        return face_list

    def get_count(self, pin: str, ver: str) -> int:
        sql = """
        SELECT COUNT(*) FROM TmpFace WHERE Pin = %s AND Ver = %s;
        """
        params = (pin.lower(), ver.lower())
        result = MySQLHelper.execute_scalar(sql, params)
        return int(result) if result else 0

    def add(self, model: TmpFaceModel) -> int:
        sql = """
        DELETE FROM TmpFace WHERE Pin = %s AND Ver = %s AND Fid = %s;"""
        params = (
            model.Pin, model.Ver, model.Fid
        )
        MySQLHelper.execute_non_query(sql, params)

        sql= """
        INSERT INTO TmpFace (Pin, Fid, Size, Valid, Tmp, Ver)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (
            model.Pin, model.Fid, model.Size, model.Valid, model.Tmp, model.Ver
        )
        return MySQLHelper.execute_non_query(sql, params)

    def delete(self, pins: List[str]) -> int:
        sql = """
        DELETE FROM TmpFace WHERE Pin IN (%s);
        """
        params = (",".join(["%s"] * len(pins)),)  # Generate placeholders for each pin
        result = MySQLHelper.execute_non_query(sql % params[0], tuple(pins))
        return result

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpFace"
        return MySQLHelper.execute_non_query(sql)
