from Dal.TmpBioDataDal import TmpBioDataDal
from Model.TmpBioDataModel import TmpBioDataModel

class TmpBioDataBll:
    def __init__(self):
        self._dal = TmpBioDataDal()

    def get(self, pin: str, type: str):
        return self._dal.get(pin, type)

    def add(self, model: TmpBioDataModel) -> int:
        if not model or not model.Pin:
            return -1
        return self._dal.add(model)

    def update(self, model: TmpBioDataModel) -> int:
        if not model or not model.Pin:
            return -1
        return self._dal.update(model)

    def is_exist(self, model: TmpBioDataModel) -> bool:
        return self._dal.is_exist(model)

    def is_exist_by_details(self, pin: str, no: str, index: str, type: str, major_ver: str, minor_ver: str) -> bool:
        return self._dal.is_exist(pin, no, index, type, major_ver, minor_ver)

    def delete_by_pin(self, pin: str) -> int:
        return self._dal.delete_by_pin(pin)

    def clear_all(self) -> int:
        return self._dal.clear_all()
