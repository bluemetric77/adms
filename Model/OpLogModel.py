from datetime import datetime

class OpLogModel:
    def __init__(self):
        self.ID = 0
        self.DeviceID = ""
        self.Operator = ""
        self.OpTime = datetime(1900, 1, 1)  # Default time: 1900-01-01 00:00:00
        self.User = ""
        self.OpType = ""
        self.Obj1 = ""
        self.Obj2 = ""
        self.Obj3 = ""
        self.Obj4 = ""
