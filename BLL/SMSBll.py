
from Dal.SMSDal import SMSDal
from Model.SMSModel import SMSModel
import pandas as pd


class SMSBll:
    def __init__(self):
        self._dal = SMSDal()

    def get_all(self, sql_where: str) -> pd.DataFrame:
        return self._dal.get_all(sql_where)

    def get(self, sms_id: str) -> SMSModel:
        return self._dal.get(sms_id)

    def add(self, model: SMSModel) -> int:
        return self._dal.add(model)

    def delete(self, sms_id: str) -> int:
        return self._dal.delete(sms_id)

    def update(self, model: SMSModel) -> int:
        return self._dal.update(model)

    def clear_all(self) -> int:
        return self._dal.clear_all()
