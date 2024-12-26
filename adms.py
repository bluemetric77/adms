import socket
import logging
import datetime

# Konfigurasi logging
logging.basicConfig(
    filename='adms_server_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Konfigurasi server
HOST = '0.0.0.0'  # Menerima koneksi dari semua interface
PORT = 8080      # Port server

def start_adms_server():
    # Membuat server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Maksimal 5 koneksi antrian
        logging.info(f"ADMS Server started on {HOST}:{PORT}")
        print(f"ADMS Server started on {HOST}:{PORT}")

        while True:
            try:
                # Menerima koneksi dari mesin absensi
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    logging.info(f"Connection established with {client_address}")
                    print(f"Connection established with {client_address}")

                    # Menerima data dari mesin absensi
                    data = client_socket.recv(1024).decode('utf-8')
                    if data:
                        logging.info(f"Received data from {client_address}: {data}")
                        print(f"Received data from {client_address}: {data}")

                        # Membalas mesin absensi
                        response = "Data received successfully"
                        client_socket.sendall(response.encode('utf-8'))

            except Exception as e:
                logging.error(f"Error: {e}")
                print(f"Error: {e}")

if __name__ == '__main__':
    start_adms_server()
