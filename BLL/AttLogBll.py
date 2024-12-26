from datetime import datetime
from Dal.AttLogDal import AttLogDal
from Model.AttLogModel import AttLogModel

class AttLogBll:
    def __init__(self):
        self._dal = AttLogDal()

    def get_by_time(self, start_time: datetime, end_time: datetime, user_id: str, device_sn: str):
        return self._dal.get_by_time(start_time, end_time, user_id, device_sn)

    def clear_all(self) -> int:
        return self._dal.clear_all()

    def add(self, attlog: AttLogModel) -> int:
        if self._dal.is_exist(attlog.PIN, attlog.AttTime):
            return 0
        return self._dal.add(attlog)
