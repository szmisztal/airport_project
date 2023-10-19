import random
import socket as s
import schedule
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils


class Airplane:
    def __init__(self, width, length, height):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.data_utils = DataUtils()
        self.is_running = True
        self.fuel = 3
        self.remaining_fuel = self.airplane_manager()
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
            print("No more fuel, plane crashed...")

    def airplane_manager(self):
        schedule.every(1).hour.do(self.time_for_landing())

    @classmethod
    def initial_airplane_co_ordinates(cls):
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

    def establish_co_ordinates(self):
        co_ordinates_dict = {
            "FIRST CO-ORDINATES": {
                "width": self.width,
                "length": self.length,
                "height": self.height
            }
        }
        return co_ordinates_dict

    def read_airport_response(self, dict_data):
        deserialized_data = self.data_utils.deserialize_json(dict_data)
        for key, value in deserialized_data.items():
            print(f">>> {key}: {value}")

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            airport_response = client_socket.recv(self.BUFFER)
            self.read_airport_response(airport_response)
            airplane_co_ordinates = self.establish_co_ordinates()
            airplane_co_ordinates_json = self.data_utils.serialize_to_json(airplane_co_ordinates)
            client_socket.sendall(airplane_co_ordinates_json)
            # while self.is_running:

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    co_ordinates = Airplane.initial_airplane_co_ordinates()
    airplane = Airplane(**co_ordinates)
    print("AIRPORT ON RADAR...")
    airplane.start()
