from typing import List
from Model.TmpBioDataModel import TmpBioDataModel  # Assuming TmpBioDataModel is defined elsewhere
from Dal.MySQLHelper import MySQLHelper
class TmpBioDataDal:
    def __init__(self):
        pass

    def get(self, pin: str, type: str) -> List[TmpBioDataModel]:
        sql = """
        SELECT * FROM TmpBioData WHERE Pin = %s AND Type = %s;
        """
        params = (pin, type)
        result = MySQLHelper.execute_query(sql, params)

        if not result:
            return []

        bio_list = []
        for row in result:
            bio = TmpBioDataModel()
            bio.ID = int(row['ID'])
            bio.Pin = row['Pin']
            bio.No = row['No']
            bio.Index = row['Index']
            bio.Valid = row['Valid']
            bio.Duress = row['Duress']
            bio.Type = row['Type']
            bio.MajorVer = row['MajorVer']
            bio.MinorVer = row['MinorVer']
            bio.Format = row['Format']
            bio.Tmp = row['Tmp']
            bio_list.append(bio)

        return bio_list

    def get_with_condition(self, sql_where: str) -> List[dict]:
        sql_where = "" if not sql_where else f"WHERE {sql_where}"
        sql = f"SELECT * FROM TmpBioData {sql_where};"
        return MySQLHelper.execute_query(sql)

    def add(self, model: TmpBioDataModel) -> int:
        if self.is_exist(model):
            return self.update(model)

        sql = """
        INSERT INTO TmpBioData (Pin, No, Index, Valid, Duress, Type, MajorVer, MinorVer, Format, Tmp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            model.Pin.lower(), model.No, model.Index, model.Valid, model.Duress,
            model.Type.lower(), model.MajorVer.lower(), model.MinorVer.lower(),
            model.Format, model.Tmp
        )
        return MySQLHelper.execute_non_query(sql, params)

    def update(self, model: TmpBioDataModel) -> int:
        sql = """
        UPDATE TmpBioData
        SET Valid = %s, Duress = %s, Format = %s, Tmp = %s
        WHERE Pin = %s AND No = %s AND Index = %s AND Type = %s
              AND MajorVer = %s AND MinorVer = %s;
        """
        params = (
            model.Valid, model.Duress, model.Format, model.Tmp,
            model.Pin, model.No, model.Index, model.Type.lower(),
            model.MajorVer.lower(), model.MinorVer.lower()
        )
        return MySQLHelper.execute_non_query(sql, params)

    def is_exist(self, model: TmpBioDataModel) -> bool:
        return self.is_exist_by_params(model.Pin, model.No, model.Index, model.Type, model.MajorVer, model.MinorVer)

    def is_exist_by_params(self, pin: str, no: str, index: str, type: str, major_ver: str, minor_ver: str) -> bool:
        sql = """
        SELECT 1 FROM TmpBioData
        WHERE Pin = %s AND No = %s AND Index = %s AND Type = %s
              AND MajorVer = %s AND MinorVer = %s;
        """
        params = (pin, no, index, type.lower(), major_ver.lower(), minor_ver.lower())
        result = MySQLHelper.execute_query(sql, params)
        return bool(result)

    def delete_by_pin(self, pin: str) -> int:
        sql = "DELETE FROM TmpBioData WHERE Pin = %s;"
        params = (pin,)
        return MySQLHelper.execute_non_query(sql, params)

    def clear_all(self) -> int:
        sql = "DELETE FROM TmpBioData"
        return MySQLHelper.execute_non_query(sql)
