from Dal.OpLogDal import OpLogDal
from Model.OpLogModel import OpLogModel
from typing import List
import pandas as pd
from datetime import datetime


class OpLogBll:
    def __init__(self):
        self._dal = OpLogDal()

    def get(self) -> List[OpLogModel]:
        return self._dal.get()

    def get_all(self) -> pd.DataFrame:
        return self._dal.get_all()

    def get_oplog_by_time(self, start_time: datetime, end_time: datetime, dev_sn: str) -> pd.DataFrame:
        return self._dal.get_oplog_by_time(start_time, end_time, dev_sn)

    def clear_all(self) -> int:
        return self._dal.clear_all()

    def add(self, oplog: OpLogModel) -> int:
        return self._dal.add(oplog)
