import socket as s
import time
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from airplane import Airplane
from communication_utils import ClientProtocols
from math_patterns import euclidean_formula, movement_formula


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.data_utils = DataUtils()
        self.is_running = True
        self.communication_utils = ClientProtocols()
        self.airplane = Airplane(Airplane.establish_init_airplane_coordinates())

    def read_message_from_server(self, data):
        deserialized_data = self.data_utils.deserialize_json(data)
        print(f">>> {deserialized_data['message']} {deserialized_data['body']}.")
        return deserialized_data

    def send_message_to_server(self, client_socket, data):
        client_request = self.data_utils.serialize_to_json(data)
        client_socket.sendall(client_request)

    def initial_correspondence_with_server(self, client_socket):
        server_response_json = client_socket.recv(self.BUFFER)
        server_response = self.read_message_from_server(server_response_json)
        if "Airport`s full: " in server_response["message"] and "You have to fly to another..." in server_response["body"]:
            return None
        else:
            self.airplane.id = server_response["id"]
            coordinates = self.communication_utils.coordinates_protocol(
                {"x": self.airplane.x,
                 "y": self.airplane.y,
                 "z": self.airplane.z}
            )
            self.send_message_to_server(client_socket, coordinates)
            points_for_airplane_json = client_socket.recv(self.BUFFER)
            points = self.read_message_from_server(points_for_airplane_json)["body"]
            self.airplane.set_points(points)
            airplane_obj = self.communication_utils.airplane_object_protocol(self.airplane.parse_airplane_obj_to_json())
            self.send_message_to_server(client_socket, airplane_obj)
            server_response_json = client_socket.recv(self.BUFFER)
            coordinates = self.read_message_from_server(server_response_json)
            return coordinates

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            print("CLIENT`S UP...")
            client_socket.connect((HOST, PORT))
            welcome_message_from_server = self.initial_correspondence_with_server(client_socket)
            if welcome_message_from_server == None:
                self.stop(client_socket)
            else:
                initial_landing_point_coordinates = welcome_message_from_server["coordinates"]
                while self.is_running:
                    fly_to_initial_landing_point = self.airplane.fly_to_target(initial_landing_point_coordinates)
                    if fly_to_initial_landing_point:
                        coordinates = self.communication_utils.coordinates_protocol(
                            {"x": self.airplane.x,
                             "y": self.airplane.y,
                             "z": self.airplane.z}
                        )
                        self.send_message_to_server(client_socket, coordinates)
                        time.sleep(1)
                    elif not fly_to_initial_landing_point:
                        self.send_message_to_server(client_socket,
                                                    self.communication_utils.reaching_the_target_protocol("Initial landing point"))

    def stop(self, client_socket):
        print("CLIENT`S OUT...")
        self.is_running = False
        client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.start()
