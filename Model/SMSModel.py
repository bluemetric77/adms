from datetime import datetime

class SMSModel:
    def __init__(self):
        self.ID = 0
        self.SMSId = 0
        self.Type = 254
        self.BeginTime = datetime(1900, 1, 1)  # Default time: 1900-01-01 00:00:00
        self.ValidTime = 60
        self.Content = ""
        self.UserID = ""
