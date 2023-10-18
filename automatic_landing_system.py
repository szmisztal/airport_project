import socket as s
import random
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from airplane import Airplane


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
        self.airport_width = 5000
        self.airport_length = 5000
        self.airport_height = 5000

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
            with client_socket:
                while self.is_running:
                    airplane = Airplane(10000, 10000, random.randint(3000, 5000))
                    self.airplanes_list.append(airplane)
