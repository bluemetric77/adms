from Dal.ErrorLogDal import ErrorLogDal
from Model.ErrorLogModel import ErrorLogModel
import pandas as pd


class ErrorLogBll:
    def __init__(self):
        self._dal = ErrorLogDal()

    def add(self, model: ErrorLogModel) -> int:
        return self._dal.add(model)

    def get_all(self, SN: str) -> pd.DataFrame:
        return self._dal.get_all(SN)

    def clear_all(self) -> int:
        return self._dal.clear_all()
