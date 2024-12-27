import socket
import threading
import time
import re
import os
import base64
from datetime import datetime,timezone

from BLL.AttLogBll import AttLogBll
from BLL.DeviceBll import DeviceBll
from BLL.DeviceCmdBll import DeviceCmdBll
from BLL.OpLogBll import OpLogBll
from BLL.UserInfoBll import UserInfoBll
from BLL.TmpFaceBll import TmpFaceBll
from BLL.TmpBioPhotoBll import TmpBioPhotoBll
from BLL.ErrorLogBll import ErrorLogBll
from BLL.TmpFPBll import TmpFPBll

from Model.AttLogModel import AttLogModel
from Model.DeviceModel import DeviceModel,BioType
from Model.OpLogModel import OpLogModel
from Model.TmpBioDataModel import TmpBioDataModel
from Model.TmpBioPhotoModel import TmpBioPhotoModel
from Model.TmpFaceModel import TmpFaceModel
from Model.TmpFPModel import TmpFPModel
from Model.UserInfoModel import UserInfoModel
from Model.ErrorLogModel import ErrorLogModel

from ServerInfo import ServerInfo
from Utils.Tools import Tools
from Utils.Log import Log

class TCPServer:
    def __init__(self, server_ip, port, max_buffer_size=1024):
        self.server_ip = server_ip
        self.port = port
        self.max_buffer_size = max_buffer_size
        self.listening = False
        self.server_socket = None
        self.on_new_machine = None
        self._device_bll = None
        self._device_cmd_bll = None  
        self._attlog_bll = None   
        self._oplog_bll = None   
        self._userinfo_bll = None
        self._face_bll =None
        self._biophoto_bll = None
        self._errorlog_bll = None
        self._fp_bll = None

    @property
    def device_bll(self):
        if self._device_bll is None:
            self._device_bll = DeviceBll()
        return self._device_bll

    @property
    def device_cmd_bll(self):
        if self._device_cmd_bll is None:
            self._device_cmd_bll = DeviceCmdBll()
        return self._device_cmd_bll
    
    @property
    def attlog_bll(self):
        if self._attlog_bll is None:
            self._attlog_bll = AttLogBll()
        return self._attlog_bll  

    @property
    def oplog_bll(self):
        if self._oplog_bll is None:
            self._oplog_bll = OpLogBll()
        return self._oplog_bll   

    @property
    def userinfo_bll(self):
        if self._userinfo_bll is None:
            self._userinfo_bll = UserInfoBll()
        return self._userinfo_bll           

    @property
    def face_bll(self):
        if self._face_bll is None:
            self._face_bll = TmpFaceBll()
        return self._face_bll           

    @property
    def biophoto_bll(self):
        if self._biophoto_bll is None:
            self._biophoto_bll = TmpBioPhotoBll()
        return self._biophoto_bll  
    

    @property
    def errorlog_bll(self):
        if self._errorlog_bll is None:
            self._errorlog_bll = ErrorLogBll()
        return self._errorlog_bll     
    
    @property
    def fp_bll(self):
        if self._fp_bll is None:
            self._fp_bll = TmpFPBll()
        return self._fp_bll    
     
    def start_listening(self):
        try:
            # Inisialisasi server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.port))
            self.server_socket.listen(5)
            self.listening = True
            print(f"Server listening on {self.server_ip}:{self.port}")

            while self.listening:
                try:
                    # Menerima koneksi masuk
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Connection received from {client_address}")

                    # Konfigurasi buffer
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.max_buffer_size)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.max_buffer_size)

                    # Tunggu sebentar untuk memastikan data tersedia
                    time.sleep(0.5)

                    # Periksa apakah ada data yang diterima
                    if client_socket.recv(1, socket.MSG_PEEK):  # MSG_PEEK untuk memeriksa tanpa mengkonsumsi data
                        data = client_socket.recv(self.max_buffer_size)
                        self.analysis(data, client_socket)                        

                except Exception as e:
                    print(f"Error handling client: {e}")

        except Exception as e:
            self.listening = False
            print(f"Error starting server: {e}")
            print(f"Ensure port {self.port} is available and not blocked by firewall.")
        finally:
            if self.server_socket:
                self.server_socket.close()
                print("Server stopped.")

    def set_on_new_machine(self, callback: callable):
         self.on_new_machine = callback

    def stop_listening(self):
        if self.listening:
            self.listening = False
            if self.server_socket:
                self.server_socket.close()
                print("Server stopped listening.")

    
    def analysis(self, b_receive, end_socket):
        # Decode byte array ke string
        print(f"Server received: {b_receive.decode('utf8')}")
        Log.write_com("receive",b_receive.decode('utf8'))

        str_receive = b_receive.decode('utf-8',errors="ignore").strip().rstrip('\0')



        # Proses pesan berdasarkan kontennya
        if "cdata?" in str_receive:
            self.cdata_process(b_receive, end_socket)
        elif "getrequest?" in str_receive:
            self.get_request_process(b_receive, end_socket)
        elif "devicecmd?" in str_receive:
            self.device_cmd_process(b_receive, end_socket)
        elif "ping?" in str_receive:
            self.send_data_to_device("200 OK", "OK\r\n", end_socket)
            end_socket.close()
        else:
            self.unknown_cmd_process(end_socket)
            Log.write_log(f"Unknown message from device: {str_receive}")

    def get_time_number(self, sBuffer):
        numberstr = ""

        for char in sBuffer:
            if '0' <= char <= '9':  # Check if the character is a digit
                numberstr += char
            else:
                break

        return numberstr

    def get_value_by_name_in_push_header(self, buffer, name):
        split_str = re.split('[&? ]', buffer)
        if not split_str:
            return None

        for tmp_str in split_str:
            if f"{name}=" in tmp_str:
                return tmp_str[tmp_str.index(f"{name}=") + len(name) + 1:]
        return None
    
    def get_time_from_time_zone(self, timezone):
        try:
            # Check if the timezone starts with '-'
            if timezone[0] == '-':
                timezone = timezone[1:]  # Remove the '-' sign
                spistr = timezone.split(':')
                if len(spistr) == 2:
                    return -1 * (int(spistr[0]) * 60 + int(spistr[1]))
                elif len(spistr) == 1:
                    return -1 * (int(spistr[0]) * 60)
            else:
                spistr = timezone.split(':')
                if len(spistr) == 2:
                    return int(spistr[0]) * 60 + int(spistr[1])
                elif len(spistr) == 1:
                    return int(spistr[0]) * 60
        except:
            pass
        return 0

    def get_device_init_info(self,device=DeviceModel):
        ret_device_info = []
        time = self.get_time_from_time_zone(device.TimeZone)
        
        ret_device_info.append(f"GET OPTION FROM:{device.DevSN}\n")
        ret_device_info.append(f"Stamp={device.AttLogStamp}\n")
        ret_device_info.append(f"OpStamp={device.OperLogStamp}\n")
        ret_device_info.append(f"PhotoStamp={device.AttPhotoStamp}\n")
        ret_device_info.append(f"TransFlag={device.TransFlag}\n")
        ret_device_info.append(f"ErrorDelay={device.ErrorDelay}\n")
        ret_device_info.append(f"Delay={device.Delay}\n")
        ret_device_info.append(f"TimeZone={time}\n")
        ret_device_info.append(f"TransTimes={device.TransTimes}\n")
        ret_device_info.append(f"TransInterval={device.TransInterval}\n")
        ret_device_info.append(f"SyncTime={device.SyncTime}\n")
        ret_device_info.append(f"Realtime={device.Realtime}\n")
        ret_device_info.append(f"ServerVer={ServerInfo.VERSION} {datetime.now().strftime('%Y-%m-%d')}\n")
        ret_device_info.append(f"PushProtVer={ServerInfo.PUSH_PROT_VER}\n")
        ret_device_info.append(f"PushOptionsFlag={ServerInfo.PUSH_OPTIONS_FLAG}\n")
        ret_device_info.append(f"ATTLOGStamp={device.AttLogStamp}\n")
        ret_device_info.append(f"OPERLOGStamp={device.OperLogStamp}\n")
        ret_device_info.append(f"ATTPHOTOStamp={device.AttPhotoStamp}\n")
        ret_device_info.append("ServerName=Logtime Server\n")
        ret_device_info.append(f"MultiBioDataSupport={device.MultiBioDataSupport}\n")
        
        return ''.join(ret_device_info)

    
    def cdata_process(self, b_receive, remote_socket):
        s_buffer = b_receive.decode("ascii").strip().rstrip('\0')
        sn = self.get_value_by_name_in_push_header(s_buffer, "SN")
        reply_code = "200 OK"
        str_reply = "OK"

        if s_buffer.startswith("GET"):
            if "options=all" in s_buffer:
                reply_code, str_reply = self.init_device_connect(sn, str_reply)
                self.send_data_to_device(reply_code, str_reply, remote_socket)
                remote_socket.close()
                return
            else:
                reply_code = "400 Bad Request"
                str_reply = "Unknown Command"
                self.send_data_to_device(reply_code, str_reply, remote_socket)
                remote_socket.close()
                return

        if s_buffer.startswith("POST"):
            # Process different tables
            if "Stamp" in s_buffer and "OPERLOG" not in s_buffer and "ATTLOG" in s_buffer:
                self.att_log(s_buffer)

            if "Stamp" in s_buffer and "OPERLOG" in s_buffer and "ATTLOG" not in s_buffer:
                if "Expect: 100-continue" in s_buffer and "FP" not in s_buffer and "FACE" not in s_buffer:
                    reply_code = "100 Continue"
                    str_reply = "Continue"
                    self.send_data_to_device(reply_code, str_reply, remote_socket)
                    time.sleep(5)
                    remote_socket.close()
                    return
                self.oper_log(s_buffer)

            if "Stamp" in s_buffer and "BIODATA" in s_buffer:
                self.bio_data(s_buffer)

            if "Stamp" in s_buffer and "ERRORLOG" in s_buffer and "ATTLOG" not in s_buffer:
                self.error_log(s_buffer)

            if "Stamp" in s_buffer and "ATTPHOTO" in s_buffer:
                if "Expect: 100-continue" in s_buffer and "PIN" not in s_buffer:
                    reply_code = "100 Continue"
                    str_reply = "Continue"
                    self.send_data_to_device(reply_code, str_reply, remote_socket)
                    time.sleep(5)
                    remote_socket.close()
                    return
                self.att_photo(b_receive)

            if "Stamp" in s_buffer and "USERPIC" in s_buffer:
                self.user_pic_log(s_buffer)

            if "table=options" in s_buffer:
                self.options(s_buffer)

            self.send_data_to_device(reply_code, str_reply, remote_socket)
            remote_socket.close()


    def update_device_info(self, device :DeviceModel, str_dev_info):
        split_str = str_dev_info.split(',')

        try:
            device.DevFirmwareVersion = split_str[0].replace("%20", " ")
            device.UserCount = int(split_str[1])
            # device.fp_count = int(split_str[2])  # Assuming you may want to handle this later
            device.AttCount = int(split_str[3])
            device.DevIP = split_str[4]
        except Exception as ex:
            Log.write_log(f"Device Info Error: {str_dev_info}")

        self.device_bll.update(device)


    def get_request_process(self,b_receive, remote_socket):
        s_buffer = b_receive.decode("gb2312")
        cmd_string = "OK\r\n"
        sn = self.get_value_by_name_in_push_header(s_buffer, "SN")
        reply_code = "200 OK"

        device = self.device_bll.get(sn)

        str_dev_info = self.get_value_by_name_in_push_header(s_buffer, "INFO")
        
        if not str_dev_info:
            cmd_string = self.device_cmd_bll.send(sn) + "\r\n"
        else:
            self.update_device_info(device, str_dev_info)
            cmd_string = "OK\r\n"

        self.send_data_to_device(reply_code, cmd_string, remote_socket)
        remote_socket.close()


    def device_cmd_process(self,b_receive, remote_socket):
        s_buffer = b_receive.decode("ascii").strip('\0')
        str_receive = s_buffer
        machine_sn = s_buffer[s_buffer.index("SN=") + 3:]
        sn = machine_sn.split('&')[0]

        index = str_receive.find("ID=")
        self.send_data_to_device("200 OK", "OK\r\n", remote_socket)
        remote_socket.close()

        self.device_cmd_bll.update(str_receive[index:])


    def unknown_cmd_process(self,remote_socket):
        self.send_data_to_device("401 Unknown", "Unknown DATA", remote_socket)
        remote_socket.close()


    def send_data_to_device(self,status_code, data_str, socket):
        b_data = data_str.encode("gb2312")
        # b_data = data_str.encode("utf-8")
        header = (
            f"HTTP/1.1 {status_code}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Accept-Ranges: bytes\r\n"
            f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            f"Content-Length: {len(b_data)}\r\n\r\n"
        )
        print("Sending data to client:")
        self.send_to_browser(header.encode("gb2312"), socket)
        # self.send_to_browser(header.encode("utf-8"), socket)
        self.send_to_browser(b_data, socket)


    def send_to_browser(self, data, socket):
        error_message = None
        try:
            bytes_sent = socket.sendall(data)
            if bytes_sent == 0:
                error_message = "Socket Error: Cannot send packet"
            else:
                output=data.decode("utf-8")
                print(output)
                Log.write_com("send",output)
        except Exception as ex:
            error_message = f"Error sending data: {ex}"
            print(f"Error sending data : {ex}")

        if error_message:
            print(f"Error sending data to browser: {error_message}")
            Log.write_log(f"Error sending data to browser: {error_message}")

    def init_device_connect(self, dev_sn, rep_string):
        machine = self.device_bll.get(dev_sn)
        if machine is None:
            machine = DeviceModel()
            machine.DevSN = dev_sn
            machine.TimeZone = "34"
            if self.device_bll.add(machine)>0:
                rep_string = "OK\r\n"
                return "200 OK", rep_string
            else :                
                rep_string = "Device Unauthorized"
                return "401 Unauthorized", rep_string
        else:
            rep_string = self.get_device_init_info(machine)
            return "200 OK", rep_string
        
    def create_oplog(self, oplog, machine_sn):
        oplogstr = oplog.split('\t')
        operlog = OpLogModel()

        optype_tem = oplogstr[0]
        operlog.OpType = optype_tem[6:]
        operlog.Operator = oplogstr[1]
        operlog.OpTime = datetime.strptime(oplogstr[2], "%Y-%m-%d %H:%M:%S")  # Adjust format as needed
        operlog.Obj1 = oplogstr[3]
        operlog.Obj2 = oplogstr[4]
        operlog.Obj3 = oplogstr[5]
        operlog.Obj4 = oplogstr[6]
        operlog.User = "0"
        operlog.DeviceID = machine_sn

        return operlog

    def create_fp(self, template, sn, is_bio_data):
        tmp_fp = TmpFPModel()

        if is_bio_data:
            template = Tools.replace(template, "BIODATA", "")
            dic = Tools.get_key_values(template)

            tmp_fp.Pin = Tools.get_value_from_dic(dic, "PIN")
            tmp_fp.Fid = Tools.get_value_from_dic(dic, "No")
            tmp_fp.Valid = Tools.get_value_from_dic(dic, "Valid")
            tmp_fp.Duress = Tools.get_value_from_dic(dic, "Duress")
            major_ver = Tools.get_value_from_dic(dic, "MajorVer")

            # Get the fingerprint version from the database if not provided
            if not major_ver:
                model = self.device_bll.get(sn)
                if model is not None:
                    major_ver = model.get_bio_version(BioType.FingerPrint).split(".")[0]

            tmp_fp.MajorVer = major_ver
            tmp_fp.Tmp = Tools.get_value_from_dic(dic, "TMP")

        else:
            template = Tools.replace(template, "FP", "")
            dic = Tools.get_key_values(template)

            tmp_fp.Pin = Tools.get_value_from_dic(dic, "PIN")
            tmp_fp.Fid = Tools.get_value_from_dic(dic, "FID")
            tmp_fp.Size = Tools.try_convert_to_int32(Tools.get_value_from_dic(dic,"SIZE"))
            tmp_fp.Valid = Tools.get_value_from_dic(dic, "Valid")
            tmp_fp.Tmp = Tools.get_value_from_dic(dic, "TMP")

            if tmp_fp.Tmp.startswith("oco"):
                tmp_fp.MajorVer = "9"
            else:
                tmp_fp.MajorVer = "10"

        return tmp_fp


    def create_face(self, template, is_bio_data):
        tmp_face = TmpFaceModel()

        if is_bio_data:
            template = Tools.replace(template, "BIODATA", "")
            dic = Tools.get_key_values(template)

            tmp_face.Pin = Tools.get_value_from_dic(dic, "PIN")
            tmp_face.Fid = Tools.get_value_from_dic(dic, "No")
            tmp_face.Valid = Tools.get_value_from_dic(dic, "Valid")

            major_ver = Tools.get_value_from_dic(dic, "MajorVer")
            minor_ver = Tools.get_value_from_dic(dic, "MinorVer")
            tmp_face.Ver = f"{major_ver}.{minor_ver}"
            tmp_face.Tmp = Tools.get_value_from_dic(dic, "TMP")
        else:
            template = Tools.replace(template, "FACE", "")
            dic = Tools.get_key_values(template)

            tmp_face.Pin = Tools.get_value_from_dic(dic, "PIN")
            tmp_face.Fid = Tools.get_value_from_dic(dic, "FID")
            tmp_face.Size = Tools.try_convert_to_int32(Tools.get_value_from_dic(dic,"SIZE"))
            tmp_face.Valid = Tools.get_value_from_dic(dic, "VALID")
            tmp_face.Tmp = Tools.get_value_from_dic(dic, "TMP")

        return tmp_face

    def create_palm(self, template):
        template = Tools.replace(template, "BIODATA", "")
        dic = Tools.get_key_values(template)

        tmp_palm = TmpBioDataModel()
        tmp_palm.Pin = Tools.get_value_from_dic(dic, "PIN")
        tmp_palm.No = Tools.get_value_from_dic(dic, "No")
        tmp_palm.Index = Tools.get_value_from_dic(dic, "Index")
        tmp_palm.Valid = Tools.get_value_from_dic(dic, "Valid")
        tmp_palm.Duress = Tools.get_value_from_dic(dic, "Duress")
        tmp_palm.Type = Tools.get_value_from_dic(dic, "Type")
        tmp_palm.MajorVer = Tools.get_value_from_dic(dic, "MajorVer")
        tmp_palm.MinorVer = Tools.get_value_from_dic(dic, "MinorVer")
        tmp_palm.Format = Tools.get_value_from_dic(dic, "Format")
        tmp_palm.Tmp = Tools.get_value_from_dic(dic, "TMP")

        return tmp_palm

    def create_bio_photo(self, bio_photo_string):
        bio_photo_string = Tools.replace(bio_photo_string, "BIOPHOTO", "")
        dic = Tools.get_key_values(bio_photo_string)

        biophoto = TmpBioPhotoModel()
        biophoto.Pin = Tools.get_value_from_dic(dic, "PIN")
        biophoto.FileName = Tools.get_value_from_dic(dic, "FileName")
        biophoto.Type = Tools.get_value_from_dic(dic, "Type")
        biophoto.Size = Tools.try_convert_to_int32(Tools.get_value_from_dic(dic, "Size"))
        biophoto.Content = Tools.get_value_from_dic(dic, "Content")

        return biophoto


    def create_user_info(self, user_string,sn="1"):
        user_string = Tools.replace(user_string, "USER", "")
        dic = Tools.get_key_values(user_string)

        user = UserInfoModel()
        user.PIN = Tools.get_value_from_dic(dic, "PIN")
        user.UserName = Tools.get_value_from_dic(dic, "Name")
        user.Pri = Tools.get_value_from_dic(dic, "Pri")
        user.Passwd = Tools.get_value_from_dic(dic, "Passwd")
        user.IDCard = Tools.get_value_from_dic(dic, "Card")
        user.Grp = Tools.get_value_from_dic(dic, "Grp")
        user.TZ = Tools.get_value_from_dic(dic, "TZ")
        user.DevSN = sn

        return user

    def oper_log(self, sBuffer):
        machineSN = sBuffer[sBuffer.index("SN=") + 3:]
        SN = machineSN.split('&')[0]
        if not SN:
            return

        machinestamp = sBuffer[sBuffer.index("Stamp=") + 6:]
        Stamp = self.get_time_number(machinestamp)  

        # Update machine oplogStamp
        self.device_bll.update_oper_log_stamp(Stamp,SN)    

        operindex = sBuffer.find("\r\n\r\n")
        operstr = sBuffer[operindex + 4:]
        self.separate_operlog_data(operstr, SN)

    def separate_operlog_data(self, datastr, SN):
        try:
            strlist = datastr.split('\n')
            for i in strlist:
                tmpstr = i.strip()

                if "OPLOG " in tmpstr:
                    self.oplog_bll.add(self.create_oplog(tmpstr,SN))
                elif tmpstr.split(' ')[0] == "USER":
                    if "PIN" in tmpstr.upper():
                        user=self.create_user_info(tmpstr,SN)
                        user_model = self.userinfo_bll.get(user.PIN)
                        if user_model is None:
                           self.userinfo_bll.add(user)
                        else:
                           self.userinfo_bll.update(user)
                elif tmpstr.split(' ')[0] == "FP":
                    if "PIN" in tmpstr.upper():
                        fp=self.create_fp(tmpstr,SN,False)
                        self.fp_bll.add(fp)
                elif tmpstr.split(' ')[0] == "FACE":
                    if "PIN" in tmpstr.upper():
                        self.face_bll.add(self.create_face(tmpstr, False))
                elif tmpstr.split(' ')[0] == "BIOPHOTO":
                    if "PIN" in tmpstr.upper():
                        self.biophoto_bll.add(self.create_bio_photo(tmpstr))
        except Exception as ex:
            Log.write_log(str(ex))


    def bio_data(self, s_buffer: str):
        machine_sn = s_buffer[s_buffer.index("SN=") + 3:]
        sn = machine_sn.split('&')[0]

        machine_stamp = s_buffer[s_buffer.index("Stamp=") + 6:]
        Stamp = self.get_time_number(machine_stamp)  

        bio_index = s_buffer.index("\r\n\r\n") + 4
        bio_str = s_buffer[bio_index:]

        self.separate_bio_data(bio_str, sn)

    def separate_bio_data(self, data_str: str, sn: str):
        try:
            str_list = data_str.split('\n')
            for tmp_str in str_list:
                tmp_str = tmp_str.strip()
                if not tmp_str:
                    continue

                bio_type_str = tmp_str.split('\t')[5].split('=')[1]
                bio_type = BioType[bio_type_str]  # Assuming BioType is an Enum-like structure

                if bio_type == BioType.Comm:
                    pass
                elif bio_type == BioType.FingerPrint:
                    if "PIN" in tmp_str.upper():
                        fp=self.create_fp(tmp_str,sn,True)
                        self.fp_bll.add(fp)
                elif bio_type == BioType.Face:
                    if "PIN" in tmp_str.upper():
                        self.face_bll.add(self.create_face(tmp_str, True))
                elif bio_type == BioType.VocalPrint:
                    pass
                elif bio_type == BioType.Iris:
                    pass
                elif bio_type == BioType.Retina:
                    pass
                elif bio_type == BioType.PalmPrint:
                    pass
                elif bio_type == BioType.FingerVein:
                    pass
                elif bio_type == BioType.Palm:
                    if "PIN" in tmp_str.upper():
                        self.biophoto_bll.add(self.create_palm(tmp_str))
                elif bio_type == BioType.VisilightFace:
                    pass
        except Exception as ex:
            Log.write_log(str(ex))

    def error_log(self, sBuffer):
        machineSN = sBuffer[sBuffer.index("SN=") + 3:]
        SN = machineSN.split('&')[0]

        machinestamp = sBuffer[sBuffer.index("Stamp=") + 6:]
        Stamp =self.get_time_number(machinestamp)
          
        # Update machine oplogStamp
        self.device_bll.update_error_log_stamp(Stamp, SN)

        errorindex = sBuffer.find("\r\n\r\n")
        errorstr = sBuffer[errorindex + 4:]

        self.separate_error_data(self,errorstr, SN)

    def separate_error_data(self,datastr, SN):
        try:
            strlist = datastr.split('\n')
            for i in strlist:
                tmpstr = i.strip()
                if "ERRORLOG " in tmpstr:
                    self.save_error_log(tmpstr, SN)
        except Exception as ex:
            print(ex)

    def save_error_log(self,erlog, machineSN):
        self.errorlog_bll.add(self.create_error_log(erlog, machineSN))

    def create_error_log(self, erlog: str, machine_sn: str):
        erlog_str = erlog.split('\t')
        erlog_model = ErrorLogModel()

        temp = erlog_str[0]
        erlog_model.ErrCode = temp[8:].split('=')[1]
        erlog_model.ErrMsg = erlog_str[1].split('=')[1]
        erlog_model.DataOrigin = erlog_str[2].split('=')[1]
        erlog_model.CmdId = erlog_str[3].split('=')[1]
        erlog_model.Additional = erlog_str[4].split('=')[1]
        erlog_model.DeviceID = machine_sn

        return erlog_model

    def options(self, sBuffer):

        machineSN = sBuffer[sBuffer.find("SN=") + 3:]
        SN = machineSN.split('&')[0]
        if not SN:
            return

        attindex = sBuffer.find("\r\n\r\n", 1)
        strOptions = sBuffer[attindex + 4:]

        if not strOptions:
            return

        device = self.get_device_model_by_options(SN, strOptions)
        # Update the device model
        self.device_bll.update(device)


    def get_device_model_by_options(self, devSN, strOptions):
        device = self.device_bll.get(devSN)

        self.format_bio_data(strOptions)
        
        Tools.init_model(device, strOptions)

        return device


    def format_bio_data(self, options):
        if not options:
            return

        # Define the default values for bio data
        val_multi_bio_data_support = "0:0:0:0:0:0:0:0:0:0"
        val_multi_bio_photo_support = "0:0:0:0:0:0:0:0:0:0"
        val_multi_bio_version = "0:0:0:0:0:0:0:0:0:0"
        val_multi_bio_count = "0:0:0:0:0:0:0:0:0:0"
        val_max_multi_bio_data_count = "0:0:0:0:0:0:0:0:0:0"
        val_max_multi_bio_photo_count = "0:0:0:0:0:0:0:0:0:0"

        options = options.replace("~", "")
        arr_info = options.split(",")

        for info in arr_info:
            arr_key_val = info.split('=')
            if len(arr_key_val) != 2:
                continue

            key = arr_key_val[0].strip()
            val = arr_key_val[1].strip()
            if not val or val == "0":
                continue

            # Fingerprint
            if key.lower() == "fingerfunon":
                self.update_option_val(BioType.FingerPrint, val, ref=val_multi_bio_data_support)
            elif key.lower() == "fpversion":
                self.update_option_val(BioType.FingerPrint, val, ref=val_multi_bio_version)
            elif key.lower() == "fpcount":
                self.update_option_val(BioType.FingerPrint, val, ref=val_multi_bio_count)
            elif key.lower() == "maxfingercount":
                self.update_option_val(BioType.FingerPrint, val, ref=val_max_multi_bio_data_count)

            # Face
            elif key.lower() == "facefunon":
                self.update_option_val(BioType.Face, val, ref=val_multi_bio_data_support)
                self.update_option_val(BioType.VisilightFace, val, ref=val_multi_bio_data_support)
            elif key.lower() == "faceversion":
                self.update_option_val(BioType.Face, val, ref=val_multi_bio_version)
            elif key.lower() == "facecount":
                self.update_option_val(BioType.Face, val, ref=val_multi_bio_count)
            elif key.lower() == "maxfacecount":
                self.update_option_val(BioType.Face, val, ref=val_max_multi_bio_data_count)

            # Finger vein
            elif key.lower() == "fvfunon":
                self.update_option_val(BioType.FingerVein, val, ref=val_multi_bio_data_support)
            elif key.lower() == "fvversion":
                self.update_option_val(BioType.FingerVein, val, ref=val_multi_bio_version)
            elif key.lower() == "fvcount":
                self.update_option_val(BioType.FingerVein, val, ref=val_multi_bio_count)
            elif key.lower() == "maxfvcount":
                self.update_option_val(BioType.FingerVein, val, ref=val_max_multi_bio_data_count)

            # Palm (Palm vein)
            elif key.lower() == "pvfunon":
                self.update_option_val(BioType.Palm, val, ref=val_multi_bio_data_support)
            elif key.lower() == "pvversion":
                self.update_option_val(BioType.Palm, val, ref=val_multi_bio_version)
            elif key.lower() == "pvcount":
                self.update_option_val(BioType.Palm, val, ref=val_multi_bio_count)
            elif key.lower() == "maxpvcount":
                self.update_option_val(BioType.Palm, val, ref=val_max_multi_bio_data_count)

            # Visible light (Face)
            elif key.lower() == "visilightfun":
                self.update_option_val(BioType.VisilightFace, val, ref=val_multi_bio_data_support)

        options += f",MultiBioDataSupport={val_multi_bio_data_support}" \
                f",MultiBioPhotoSupport={val_multi_bio_photo_support}" \
                f",MultiBioVersion={val_multi_bio_version}" \
                f",MultiBioCount={val_multi_bio_count}" \
                f",MaxMultiBioDataCount={val_max_multi_bio_data_count}" \
                f",MaxMultiBioPhotoCount={val_max_multi_bio_photo_count}"


    def update_option_val(self, bio_type, val, ref):
        arr_val = ref.split(':')
        t = bio_type
        if t >= len(arr_val):
            return ref

        arr_val[t] = val
        ref = ':'.join(arr_val)

        return ref
    
    def att_log(self, s_buffer):
        machine_sn = s_buffer[s_buffer.index("SN=") + 3:]
        sn = machine_sn.split('&')[0]

        # Extract and convert timestamp
        machine_stamp = s_buffer[s_buffer.index("Stamp=") + 6:]
        stamp = self.extract_stamp(machine_stamp, " ")

        # Update machine attlog stamp
        self.device_bll.update_att_log_stamp(stamp, sn)

        # Process attendance log data
        att_index = s_buffer.find("\r\n\r\n")
        if att_index != -1:
            att_str = s_buffer[att_index + 4:]
            self.att_log_process(att_str, sn)

    def att_log_process(self, att_str, machine_sn):
        try:
            str_list = att_str.split("\n")
            for line in str_list:
                if not line.strip():
                    continue
                att_model=self.create_att_log(line.strip(), machine_sn)
                self.attlog_bll.add(att_model)
        except Exception as ex:
            Log.write_log(str(ex))

    def create_att_log(self, att_log, machine_sn):
        att_log_str = att_log.split('\t')
        att_log_model = AttLogModel()

        att_log_model.PIN = att_log_str[0]
        att_log_model.AttTime = datetime.strptime(att_log_str[1], '%Y-%m-%d %H:%M:%S')  # Adjust format as needed
        att_log_model.Status = att_log_str[2]
        att_log_model.Verify = att_log_str[3]
        att_log_model.DeviceID = machine_sn

        try:
            att_log_model.WorkCode = att_log_str[4]
        except IndexError:
            att_log_model.WorkCode = "0"

        if len(att_log_str) > 8:
            try:
                att_log_model.MaskFlag = int(att_log_str[7])
            except ValueError:
                att_log_model.MaskFlag = None
            att_log_model.Temperature = att_log_str[8]

        return att_log_model

    def att_photo(self, b_receive):
        str_receive = b_receive.decode('ascii')
        img_receive = bytearray(len(b_receive))

        tmp_str = str_receive.split('\n')
        str_image_number = ""

        for line in tmp_str:
            if "PIN=" in line:
                str_image_number = line
                break

        machine_sn_start = str_receive.find("SN=") + 3
        machine_sn = str_receive[machine_sn_start:]
        sn = machine_sn.split('&')[0]

        stamp_start = str_receive.find("Stamp=") + 6
        machine_stamp = str_receive[str_receive.index("Stamp=") + 6:]
        stamp = self.extract_stamp(machine_stamp, " ")

        # Update the machine's AttPhotoStamp
        self.device_bll.update_att_photo_stamp(stamp, sn)

        img_rec_index = str_receive.find("uploadphoto") + 12
        img_receive = b_receive[img_rec_index:]

        current_directory = os.getcwd()
        capture_directory = os.path.join(current_directory, "Capture")
        os.makedirs(capture_directory, exist_ok=True)  # Create directory if it doesn't exist
        file_path = os.path.join(capture_directory, str_image_number.replace("PIN=", ""))

        with open(file_path, "wb") as image_file:
            image_file.write(img_receive)

        print(f"Image saved at {file_path}")

    def workcode_log(self, s_buffer):
        machine_sn = self.get_substring_after(s_buffer, "SN=", "&")
        usin_index = s_buffer.find("\r\n\r\n")
        if usin_index != -1:
            usin_str = s_buffer[usin_index + 4:]
            self.workcode_log_process(usin_str)

    def workcode_log_process(self, s_buffer):
        try:
            if not s_buffer.strip():
                return
            usin_index = s_buffer.find("\n")
            if usin_index != -1:
                usin_str = s_buffer[:usin_index]
                if "WORKCODE" in usin_str:
                    self.save_workcode(usin_str)
                self.workcode_log_process(s_buffer[usin_index + 1:])
        except Exception as ex:
            Log.write_log(str(ex))

    def save_workcode(self, usin_log):
        if "Code" in usin_log:
            code = usin_log[:usin_log.find("\t")].replace("WORKCODE Code=", "")
            workname = usin_log[usin_log.find("\t") + 1:].replace("Name=", "")
            workcode = {"WorkCode": code, "WorkName": workname}
            if self.on_new_workcode:
                self.on_new_workcode(workcode)

    def user_pic_log(self, s_buffer):
        machine_sn = self.get_substring_after(s_buffer, "SN=", "&")
        stamp = self.extract_stamp(s_buffer, " ")
        usin_index = s_buffer.find("\r\n\r\n")
        if usin_index != -1:
            usin_str = s_buffer[usin_index + 4:]
            self.user_pic_log_process(usin_str)

    def user_pic_log_process(self, s_buffer):
        try:
            usin_index = s_buffer.find("\n")
            if usin_index != -1:
                usin_str = s_buffer[:usin_index]
                self.save_user_pic(usin_str)
                self.user_pic_log_process(s_buffer[usin_index + 1:])
        except Exception:
            pass

    def save_user_pic(self, usin_log):
        if "PIN" in usin_log and "FileName" in usin_log:
            parts = usin_log.split("\t")
            user_pin = parts[0].replace("USER PIN=", "")
            file_name = parts[1].replace("FileName=", "")
            file_path = os.path.join(os.getcwd(), "Photo", f"{file_name}.txt")
            with open(file_path, "w") as f:
                f.write(parts[3])
            self.base64_string_to_image(file_path)

    def base64_string_to_image(self, file_path):
        try:
            with open(file_path, "r") as f:
                image_data = base64.b64decode(f.read())
            image_path = file_path.replace(".txt", ".jpg")
            with open(image_path, "wb") as f:
                f.write(image_data)
        except Exception as ex:
            print(f"Failed to convert base64 to image: {ex}")

    def get_substring_after(self, s, start_key, end_char=""):
        start_index = s.find(start_key) + len(start_key)
        if end_char:
            end_index = s.find(end_char, start_index)
            return s[start_index:end_index]
        return s[start_index:]

    def extract_stamp(self, s, key):
        stamp = ""
        try:
            #machine_stamp = self.get_substring_after(s, key," ")
            stamp = s.split(" ")[0]
        except:
            pass
        return stamp



# Jalankan server
if __name__ == "__main__":
    server = TCPServer(server_ip="103.127.136.45", port=8080, max_buffer_size=1024 * 1024 * 2)
    server_thread = threading.Thread(target=server.start_listening, daemon=True)
    server_thread.start()

    try:
        while True:
            time.sleep(1)  # Biarkan server tetap berjalan
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.listening = False
