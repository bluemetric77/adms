from datetime import datetime

class AttLogModel:
    def __init__(self):
        self.PIN = "1"
        self.AttTime = datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.DeviceID = "0"
        self.Status = "0"
        self.Verify = "0"
        self.Reserved1 = "0"
        self.Reserved2 = "0"
        self.WorkCode = "0"
        self.ID = 0
        self.MaskFlag = 0
        self.Temperature = ""