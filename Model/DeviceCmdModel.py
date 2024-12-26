from datetime import datetime

class DeviceCmdModel:
    def __init__(self):
        self.DevSN = "1"
        self.CommitTime = datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.Content = ""
        self.ResponseTime = datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.TransTime = datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.ReturnValue = ""

