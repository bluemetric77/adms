from typing import List
from Dal.TmpFveinDal import TmpFveinDal

class TmpFveinBll:
    def __init__(self):
        self._dal = TmpFveinDal()

    def get(self, pins: List[str], ver: str) -> List[dict]:
        return self._dal.get(pins, ver)

    def get_count(self, pin: str, ver: str) -> int:
        return self._dal.get_count(pin, ver)

    def add(self, model: dict) -> int:
        return self._dal.add(model)

    def delete(self, pins: List[str]) -> int:
        return self._dal.delete(pins)

    def clear_all(self) -> int:
        return self._dal.clear_all()
