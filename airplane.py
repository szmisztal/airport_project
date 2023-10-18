import random
import socket as s
import schedule
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Airplane:
    def __init__(self, width, length, height):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.is_running = True
        self.fuel = 3
        self.remaining_fuel = self.fuel_manager()
        self.width = width
        self.length = length
        self.height = height

    @classmethod
    def create_airplane_object(cls, co_ordinates_dict):
        airplane = cls(**co_ordinates_dict)
        return airplane

    def time_for_landing(self):
        self.fuel -= 1
        if self.fuel == 0:
            self.stop()

    def fuel_manager(self):
        schedule.every(1).hour.do(self.time_for_landing())

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            # while self.is_running:

    def stop(self):
        self.is_running = False
        print("No more fuel, plane crashed...")
