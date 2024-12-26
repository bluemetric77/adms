from typing import List
from Dal.TmpFaceDal import TmpFaceDal
class TmpFaceBll:
    def __init__(self):
        self._dal = TmpFaceDal()

    def get(self, pin: str) -> List[dict]:
        return self._dal.get(pin)

    def get_count(self, pin: str, ver: str) -> int:
        return self._dal.get_count(pin, ver)

    def add(self, model: dict) -> int:
        return self._dal.add(model)

    def delete(self, pins: List[str]) -> int:
        return self._dal.delete(pins)

    def clear_all(self) -> int:
        return self._dal.clear_all()
