from typing import List
from Model.TmpBioPhotoModel import TmpBioPhotoModel  
from Dal.MySQLHelper import MySQLHelper 

class TmpBioPhotoDal:
    def __init__(self):
        pass

    def get(self, pin: str, type: str) -> List[TmpBioPhotoModel]:
        sql = """
        SELECT * FROM TmpBioPhoto WHERE Pin = %s AND Type IN (%s);
        """
        params = (pin, type)
        result = MySQLHelper.execute_query(sql, params)

        if not result:
            return []

        photo_list = []
        for row in result:
            photo = TmpBioPhotoModel()
            photo.ID = int(row['ID'])
            photo.Pin = row['Pin']
            photo.FileName = row['FileName']
            photo.Type = row['Type']
            photo.Size = int(row['Size'])
            photo.Content = row['Content']
            photo_list.append(photo)

        return photo_list

    def get_count(self, pin: str) -> int:
        sql = """
        SELECT COUNT(*) FROM TmpBioPhoto WHERE Pin = %s;
        """
        params = (pin.lower(),)
        result = MySQLHelper.execute_scalar(sql, params)
        return int(result) if result else 0

    def add(self, model: TmpBioPhotoModel) -> int:
        sql = """
        DELETE FROM TmpBioPhoto WHERE Pin = %s AND Type = %s;
        INSERT INTO TmpBioPhoto (Pin, FileName, Type, Size, Content)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (
            model.Pin, model.Type,
            model.Pin, model.FileName, model.Type, model.Size, model.Content
        )
        return MySQLHelper.execute_non_query(sql, params)

    def delete(self, pins: List[str]) -> int:
        sql = """
        DELETE FROM TmpBioPhoto WHERE Pin IN (%s);
        """
        params = (",".join(["%s"] * len(pins)),)  # Generate placeholders for each pin
        result = MySQLHelper.execute_non_query(sql % params[0], tuple(pins))
        return result

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpBioPhoto"
        return MySQLHelper.execute_non_query(sql)
