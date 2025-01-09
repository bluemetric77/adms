from datetime import datetime

class DeviceModel:
    def __init__(self):
        self.ID = -1
        self.DevSN ='iClock'
        self.DevName = "Iclock600"
        self.Delay = "10"
        self.DevFirmwareVersion = ""
        self.DevIP = "192.168.1.201"
        self.DevMac = "0C:00:00:00:B1:02"
        self.Encrypt = "0"
        self.Realtime = "1"
        self.SyncTime = 0
        self.ErrorDelay = "120"
        self.Timeout = 120
        self.TransInterval = "30"
        self.TransTimes = ""
        self.UserCount = 10000
        self.VendorName = "ZK"
        self.TransFlag = "TransData AttLog\tOpLog\tAttPhoto\tEnrollUser\tChgUser\tEnrollFP\tChgFP\tFPImag\tFACE\tUserPic\tWORKCODE\tBioPhoto"
        self.AttLogStamp = "0"
        self.AttPhotoStamp = "0"
        self.OperLogStamp = "0"
        self.TimeZone = "07:00"
        self.LastRequestTime = datetime(1900, 1, 1)
        self.IRTempDetectionFunOn = "0"
        self.MaskDetectionFunOn = "0"
        self.MultiBioDataSupport = "1:1:1:1:1:1:1:1:1:1"
        self.AttCount=0
        self.MultiBioPhotoSupport=""
        self.MultiBioVersion=""
        self.MaxMultiBioPhotoCount=""
        self.MaxMultiBioDataCount=""
        self.MultiBioCount=""

    def __str__(self):
        return self.DevSN

    def is_bio_data_support(self, bio_type):
        if not self.MultiBioDataSupport:
            return False
        arr = self.MultiBioDataSupport.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return False
        return arr[bio_type] != "0" and arr[bio_type] != ""

    def is_bio_photo_support(self, bio_type):
        if not self.MultiBioPhotoSupport:
            return False
        arr = self.MultiBioDataSupport.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return False
        return arr[bio_type] != "0" and arr[bio_type] != ""

    def get_bio_version(self, bio_type):
        version = ""
        if not self.MultiBioVersion:
            return version
        arr = self.MultiBioVersion.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return version
        return arr[bio_type]

    def get_bio_data_count(self, bio_type):
        if not self.MultiBioCount:
            return 0
        arr = self.MultiBioCount.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return 0
        return int(arr[bio_type])

    def get_bio_photo_count(self, bio_type):
        if not self.MaxMultiBioPhotoCount:
            return 0
        arr = self.MaxMultiBioPhotoCount.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return 0
        return int(arr[bio_type])

    def get_max_bio_data_count(self, bio_type):
        if not self.MaxMultiBioDataCount:
            return 0
        arr = self.MaxMultiBioDataCount.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return 0
        return int(arr[bio_type])

    def get_max_bio_photo_count(self, bio_type):
        if not self.MaxMultiBioPhotoCount:
            return 0
        arr = self.MaxMultiBioPhotoCount.split(':')
        if len(arr) != 10 or bio_type >= len(arr):
            return 0
        return int(arr[bio_type])


class BioType:
    Comm = 0
    FingerPrint = 1
    Face = 2
    VocalPrint = 3
    Iris = 4
    Retina = 5
    PalmPrint = 6
    FingerVein = 7
    Palm = 8
    VisilightFace = 9
