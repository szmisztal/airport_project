import socket as s
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
        self.airport_lane_1 = AirportLane((-2000, 2000), (500, 600), (0, 3000))
        self.airport_lane_2 = AirportLane((-2000, 2000), (-500, -600), (0, 3000))
        self.airplanes_list = []

    def max_number_of_planes(self):
        if len(self.airplanes_list) > 99:
            overload_message = {
                "The airport is full": "You have to find another"
            }
            return overload_message

    def first_message_to_airplane(self):
        start_message = {
            "STATUS": "You appeared on the radar"
        }
        return start_message

    def read_airplane_request(self, airplane_request):
        deserialized_dict = self.data_utils.deserialize_json(airplane_request)
        print(deserialized_dict)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            welcome_message = self.data_utils.serialize_to_json(self.first_message_to_airplane())
            client_socket.sendall(welcome_message)
            airplane_json = client_socket.recv(BUFFER)
            airplane_response = self.read_airplane_request(airplane_json)
            if "FIRST CO-ORDINATES" in airplane_response:
                co_ordinates = airplane_response["FIRST CO-ORDINATES"]
                airplane = Airplane(**co_ordinates)
                self.airplanes_list.append(airplane)
            # with client_socket:
            #     while self.is_running:


class AirportLane:
    def __init__(self, width, length, height ):
        self.width = width
        self.length = length
        self.height = height

    def lane_coordinates(self):
        co_ordinates_dict = {
            "width": self.width,
            "length": self.length,
            "height": self.height
        }
        return co_ordinates_dict


if __name__ == "__main__":
    airport = AutomaticLandingSystem()
    print("AIRPORT LANDING SYSTEM`S UP...")
    airport.start()
