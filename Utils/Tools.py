import datetime

class Tools:
    @staticmethod
    def find_value(content, key):
        s_ret = ''
        start_key_index = content.find(key)
        if start_key_index < 0:
            return ''
        end_tab_index = content.find("\t", start_key_index)
        if start_key_index >= 0 and end_tab_index > 0:
            s_ret = content[start_key_index:content.find('\t', start_key_index)].split('=')[1]
        elif start_key_index > 0 and end_tab_index < 0:
            s_ret = content[start_key_index:]
            s_ret = s_ret[len(key)+1:]
        return s_ret

    @staticmethod
    def union_string(keys):
        str_key = ','.join(f"'{key}'" for key in keys)
        return str_key

    @staticmethod
    def get_datetime_now():
        return datetime.datetime.now()

    @staticmethod
    def get_datetime_now_string():
        return Tools.get_datetime_now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def try_convert_to_int32(val, default_val=0):
        try:
            return int(val)
        except:
            return default_val

    @staticmethod
    def init_model(model, data):
        if model is not None:
            infos = data.split(",")
            if infos:
                for info in infos:
                    columndata = info.split('=')
                    if columndata and len(columndata) == 2 and columndata[1]:
                        columndata[0] = columndata[0].replace("~", "")
                        for pi in model.__dict__:
                            if pi.lower() == columndata[0].lower():
                                try:
                                    pvalue = columndata[1]
                                    if not pvalue.strip() or pvalue.strip().lower() == "null":
                                        pvalue = ''
                                    Tools.set_k_value(model, pvalue, pi)
                                except:
                                    pass
                                break

    @staticmethod
    def set_k_value(info, pvalue, pi):
        if isinstance(getattr(info, pi), int):
            try:
                kvalue = int(pvalue)
                setattr(info, pi, kvalue)
            except:
                pass
        elif isinstance(getattr(info, pi), str):
            setattr(info, pi, pvalue)
        elif isinstance(getattr(info, pi), datetime.datetime):
            try:
                dt = datetime.datetime.strptime(pvalue, '%Y-%m-%d %H:%M:%S')
                setattr(info, pi, dt)
            except:
                pass

    @staticmethod
    def replace(str_val, old_str, new_str, string_comparison="ignore_case"):
        idx = str_val.lower().find(old_str.lower()) if string_comparison == "ignore_case" else str_val.find(old_str)
        if idx == -1:
            return str_val

        return str_val[:idx] + new_str + str_val[idx + len(old_str):]

    @staticmethod
    def get_key_values(str_val, c_split='\t', c_split_kv='=', key_to_lower=True):
        dic = {}
        if not str_val:
            return dic

        arr = str_val.split(c_split)
        for kv in arr:
            idx = kv.find(c_split_kv)
            if idx <= 0:
                continue

            key = kv[:idx].strip()
            if key_to_lower:
                key = key.lower()

            if key and key not in dic:
                dic[key] = kv[idx + 1:]
        return dic

    @staticmethod
    def get_value_from_dic(dic, key, default_val="", key_to_lower=True):
        if not key:
            return default_val

        if key_to_lower:
            key = key.strip().lower()

        return dic.get(key, default_val)
