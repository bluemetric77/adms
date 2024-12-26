class TmpBioDataModel:
    def __init__(self, no="0", valid="1", duress="0"):
        self.ID = 0  # Default to 0, as no value was provided in the constructor
        self.No = no
        self.Pin = ""  # Default to an empty string
        self.Index = ""  # Default to an empty string
        self.Valid = valid
        self.Duress = duress
        self.Type = ""  # Default to an empty string
        self.MajorVer = ""  # Default to an empty string
        self.MinorVer = ""  # Default to an empty string
        self.Format = ""  # Default to an empty string
        self.Tmp = ""  # Default to an empty string
