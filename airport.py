import socket as s
import random
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from airplane import Airplane


class Airport:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.data_utils = DataUtils()
        self.encode_format = encode_format
        self.is_running = True
        self.lock = Lock()
        self.max_numbers_of_airplanes = 100
        self.airplanes_in_air_list = []
        self.airport_area = AirportArea(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor = AirCorridor(-3500, 3500, -250, 250, 0 , 2000)
        self.airport_lane_1 = AirportLane(-2500, 2500, 100, 150)
        self.airport_lane_2 = AirportLane(-2500, 2500, -100, -150)

    def establish_init_airplane_co_ordinates(self):
        height = random.randint(2000, 5000)
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
            "x": choose_option[0],
            "y": choose_option[1],
            "z": choose_option[2]
        }
        return co_ordinates_dict

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            with client_socket:
                while self.is_running:
                    co_ordinates = self.establish_init_airplane_co_ordinates()
                    airplane = Airplane(**co_ordinates)
                    self.airplanes_in_air_list.append(airplane)



class AirportLane:
    def __init__(self, x1, x2, y1, y2):
        self.occupied = False
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = 0


class AirportArea:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)


class AirCorridor:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)


if __name__ == "__main__":
    airport = Airport()
    airport.start()



