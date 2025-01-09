import os
import threading
import datetime


class Log:
    _lock = threading.Lock()
    _buffer = []

    @staticmethod
    def _daily_log_file():
        # Generate a log file name based on the current date
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        log_dir = "logs"  # Directory to store logs
        os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
        return os.path.join(log_dir, f"log_{date_str}.log")
    
    @staticmethod
    def _daily_com_file():
        # Generate a log file name based on the current date
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        log_dir = "logs"  # Directory to store logs
        os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
        return os.path.join(log_dir, f"com_{date_str}.log")    
    
    def write_log(msg, cache=False):
        with Log._lock:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Log._buffer.append(f"{timestamp}\n{msg}\n")

            if len("".join(Log._buffer)) > 500 or not cache:
                try:
                    log_file_path = Log._daily_log_file()
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.writelines(Log._buffer)
                    Log._buffer.clear()
                except Exception as e:
                    print(f"Failed to write log: {e}")
                    Log._buffer.clear()

    @staticmethod
    def write_logs(msg):
        Log.write_log(msg, cache=True)

    def write_com(block, msg, cache=False):
        with Log._lock:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if block=='send':
                Log._buffer.append(f"Server send data : {timestamp}\n{msg}\n")
            else:
                Log._buffer.append(f"Server receive data : {timestamp}\n{msg}\n")

            if len("".join(Log._buffer)) > 1000 or not cache:
                try:
                    log_file_path = Log._daily_com_file()
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.writelines(Log._buffer)
                    Log._buffer.clear()
                except Exception as e:
                    print(f"Failed to write communication : {e}")
                    Log._buffer.clear()

    def write_coms(block, msg):
        Log.write_com(block, msg, cache=True)

