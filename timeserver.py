from socket import *
import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s')

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break

                request = data.decode().strip()

                logging.warning(f"Received from {self.address}: {repr(request)}")

                if request.startswith("TIME"):
                    now = datetime.now()
                    waktu = now.strftime("%H:%M:%S")
                    response = f"JAM {waktu}\r\n"
                    self.connection.sendall(response.encode('utf-8'))

                elif request == "QUIT":
                    logging.warning(f"Connection from {self.address} closed by client.")
                    break

                else:
                    self.connection.sendall(b"INVALID COMMAND\r\n")
        except Exception as e:
            logging.warning(f"Error with client {self.address}: {e}")
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("Server is running on port 45000...")

        while True:
            connection, address = self.my_socket.accept()
            logging.warning(f"Accepted connection from {address}")

            client_thread = ProcessTheClient(connection, address)
            client_thread.start()
            self.clients.append(client_thread)

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
