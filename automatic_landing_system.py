import socket as s
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils


class AutomaticLandingSystem:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.lock = Lock()
        self.data_utils = DataUtils()
        self.is_running = True
        self.airport_lanes = 2
        self.airplanes_list = []
        self.width = 10000
        self.length = 10000
        self.height = 5000

    def max_number_of_planes(self):
        if len(self.airplanes_list) > 99:
            overload_message = {
                "The airport is full": "You have to find another"
            }
            return overload_message

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            client_ip = address[0]
            client_port = address[1]
            print(f"Connection from {client_ip}:{client_port}")
            # with client_socket:
            #     while self.is_running:
