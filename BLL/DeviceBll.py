from typing import List, Optional
from Model.DeviceModel import DeviceModel
from Dal.DeviceDal import DeviceDal
import pandas as pd

class DeviceBll:
    def __init__(self):
        self._dal = DeviceDal()

    def add(self, device: DeviceModel) -> int:
        return self._dal.add(device)

    def delete(self, dev_sn: str) -> int:
        return self._dal.delete(dev_sn)

    def update(self, device: DeviceModel) -> int:
        return self._dal.update(device)

    def get(self, dev_sn: str) -> Optional[DeviceModel]:
        return self._dal.get(dev_sn)

    def get_all(self, sql_where: str) -> pd.DataFrame:
        return self._dal.get_all(sql_where)

    def update_att_log_stamp(self, stamp: str, dev_sn: str):
        self._dal.update_att_log_stamp(stamp, dev_sn)

    def update_oper_log_stamp(self, stamp: str, dev_sn: str):
        self._dal.update_oper_log_stamp(stamp, dev_sn)

    def update_error_log_stamp(self, stamp: str, dev_sn: str):
        self._dal.update_error_log_stamp(stamp, dev_sn)

    def update_att_photo_stamp(self, stamp: str, dev_sn: str):
        self._dal.update_att_photo_stamp(stamp, dev_sn)

    def set_zero_stamp(self, sn_list: List[str]):
        self._dal.set_zero_stamp(sn_list)

    def set_zero_att_log_stamp(self, sn_list: List[str]):
        self._dal.set_zero_att_log_stamp(sn_list)

    def set_last_request_time(self, dev_sn: str):
        self._dal.set_last_request_time(dev_sn)

    def update_vendor_name(self, sn: str, vendor_name: str):
        self._dal.update_vendor_name(sn, vendor_name)

    def get_all_dev_sn(self) -> List[str]:
        return self._dal.get_all_dev_sn()
