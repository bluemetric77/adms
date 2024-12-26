from Dal.DeviceCmdDal import DeviceCmdDal
from Model.DeviceCmdModel import DeviceCmdModel
from typing import List
from datetime import datetime

class DeviceCmdBll:
    def __init__(self):
        self._dal = DeviceCmdDal()

    def add(self, dCmd: DeviceCmdModel):
        return self._dal.add(dCmd)

    def send(self, devSN: str) -> str:
        return self._dal.send(devSN)

    def get_by_time(self, start_time: datetime, end_time: datetime, devSN: str):
        return self._dal.get_by_time(start_time, end_time, devSN)

    def get_all(self):
        return self._dal.get_all()

    def update(self, arr_content: str):
        self._dal.update(arr_content)

    def delete(self, ids: List[str]):
        return self._dal.delete(ids)

    def clear_all(self):
        return self._dal.clear_all()
