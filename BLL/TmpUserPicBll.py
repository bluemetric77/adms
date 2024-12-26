from typing import List
from Dal.TmpUserPicDal import TmpUserPicDal

class TmpUserPicBll:
    def __init__(self):
        self._dal = TmpUserPicDal()

    def get(self, pins: List[str]) -> List[dict]:
        return self._dal.get(pins)

    def get_count(self, pin: str) -> int:
        return self._dal.get_count(pin)

    def add(self, model: dict) -> int:
        return self._dal.add(model)

    def delete(self, pins: List[str]) -> int:
        return self._dal.delete(pins)

    def clear_all(self) -> int:
        return self._dal.clear_all()
