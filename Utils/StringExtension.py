class StringExtension:
    @staticmethod
    def index_of_ex(string, value, start_index=0, case_insensitive=True):
        if case_insensitive:
            string = string.lower()
            value = value.lower()
        try:
            return string.index(value, start_index)
        except ValueError:
            return -1