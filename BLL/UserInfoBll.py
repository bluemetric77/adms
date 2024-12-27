from Dal.UserInfoDal import UserInfoDal
from Model.UserInfoModel import UserInfoModel
import pandas as pd
from typing import List

class UserInfoBll:
    def __init__(self):
        self._dal = UserInfoDal()

    def add(self, user: UserInfoModel) -> int:
        return self._dal.add(user)

    def update(self, user: UserInfoModel) -> int:
        return self._dal.update(user)

    def get(self, pin: str) -> UserInfoModel:
        return self._dal.get(pin)

    def get_multiple(self, pins: List[str]) -> List[UserInfoModel]:
        if not pins:
            return []
        return self._dal.get(pins)

    def get_all(self) -> pd.DataFrame:
        return self._dal.get_all()

    def delete(self, pins: List[str]) -> int:
        return self._dal.delete(pins)

    def clear_all(self) -> int:
        return self._dal.clear_all()
