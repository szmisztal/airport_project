import socket as s
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils


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
        self.max_numbers_of_airplanes = 100
        self.airplanes_in_air_list = []
        self.airport_area = AirportArea(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor = AirCorridor(-3500, 3500, -250, 250, 0 , 2000)
        self.airport_lane_1 = AirportLane(-2500, 2500, 100, 150)
        self.airport_lane_2 = AirportLane(-2500, 2500, -100, -150)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            # with client_socket:
            #     while self.is_running:


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




