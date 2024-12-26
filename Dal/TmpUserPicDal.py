from typing import List
from Model.TmpUserPicModel import TmpUserPicModel  
from Utils.Tools import Tools  
from Dal.MySQLHelper import MySQLHelper 

class TmpUserPicDal:
    def __init__(self):
        pass

    def get(self, pins: List[str]) -> List[TmpUserPicModel]:
        sql = """
        SELECT * FROM TmpUserPic WHERE Pin IN (%s);
        """
        params = (",".join(["%s"] * len(pins)),)
        result = MySQLHelper.execute_query(sql % params[0], tuple(pins))

        if not result:
            return []

        user_pic_list = []
        for row in result:
            user_pic = TmpUserPicModel()
            user_pic.ID = int(row['ID'])
            user_pic.Pin = row['Pin']
            user_pic.FileName = row['FileName']
            user_pic.Size = int(row['Size'])
            user_pic.Content = row['Content']
            user_pic_list.append(user_pic)

        return user_pic_list

    def get_count(self, pin: str) -> int:
        sql = """
        SELECT COUNT(*) FROM TmpUserPic WHERE Pin = %s;
        """
        params = (pin.lower(),)
        result = MySQLHelper.execute_scalar(sql, params)
        return int(result) if result else 0

    def add(self, model: TmpUserPicModel) -> int:
        sql = """
        DELETE FROM TmpUserPic WHERE Pin = %s;
        INSERT INTO TmpUserPic (Pin, FileName, Size, Content)
        VALUES (%s, %s, %s, %s);
        """
        params = (
            model.Pin, model.Pin, model.FileName, model.Size,
            model.Content
        )
        return MySQLHelper.execute_non_query(sql, params)

    def delete(self, pins: List[str]) -> int:
        sql = """
        DELETE FROM TmpUserPic WHERE Pin IN (%s);
        """
        params = (",".join(["%s"] * len(pins)),)
        result = MySQLHelper.execute_non_query(sql % params[0], tuple(pins))
        return result

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpUserPic"
        return MySQLHelper.execute_non_query(sql)
