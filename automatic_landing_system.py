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

    def initial_airplane_co_ordinates(self):
        height = random.randint(3000, 5000)
        random_int = random.randint(-5000, 5000)
        constant = 5000
        neg_constant = -5000
        possible_co_ordinates = [
            [random_int, constant, height],
            [random_int, neg_constant, height],
            [constant, random_int, height],
            [neg_constant, random_int, height]
        ]
        choose_option = random.choice(possible_co_ordinates)
        co_ordinates_dict = {
            "width": choose_option[0],
            "length": choose_option[1],
            "height": choose_option[2]
        }
        return co_ordinates_dict

    def connect_with_airplane(self):
        co_ordinates_dict = self.initial_airplane_co_ordinates()
        airplane = Airplane.create_airplane_object(co_ordinates_dict)
        self.airplanes_list.append(airplane)
        return airplane

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            with client_socket:
                while self.is_running:
                    self.connect_with_airplane()
