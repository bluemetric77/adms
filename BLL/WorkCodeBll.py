from Dal import WorkCodeDal
from Model import WorkCodeModel
import pandas as pd

class WorkCodeBll:
    def __init__(self):
        self._dal = WorkCodeDal()

    def add(self, work_code: WorkCodeModel) -> int:
        return self._dal.add(work_code)

    def delete(self, work_code: str) -> int:
        return self._dal.delete(work_code)

    def update(self, work_code: WorkCodeModel) -> int:
        return self._dal.update(work_code)

    def get_by_work_code(self, work_code: str) -> WorkCodeModel:
        return self._dal.get_by_work_code(work_code)

    def get_all(self) -> pd.DataFrame:
        return self._dal.get_all()
