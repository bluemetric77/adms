from Dal.TmpBioPhotoDal import TmpBioPhotoDal

class TmpBioPhotoBll:
    def __init__(self):
        self._dal = TmpBioPhotoDal()

    def get(self, pin, type):
        return self._dal.get(pin, type)

    def get_count(self, pin):
        return self._dal.get_count(pin)

    def add(self, model):
        return self._dal.add(model)

    def delete(self, pins):
        return self._dal.delete(pins)

    def clear_all(self):
        return self._dal.clear_all()
