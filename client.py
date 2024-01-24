import selectors
import socket as s
import time
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from airplane import Airplane
from communication_utils import ClientProtocols


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.selector = selectors.DefaultSelector()
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

    def send_airplane_coordinates(self, client_socket):
        coordinates = self.communication_utils.coordinates_protocol(
            {"x": self.airplane.x,
             "y": self.airplane.y,
             "z": self.airplane.z}
        )
        self.send_message_to_server(client_socket, coordinates)
        time.sleep(1)

    def check_events(self):
        events = self.selector.select(timeout = 0)
        if events:
            for key, mask in events:
                if key.data is None:
                    server_message_json = key.fileobj.recv(self.BUFFER)
                    server_message = self.read_message_from_server(server_message_json)
                    return server_message

    def events_service(self):
        event_message = self.check_events()
        if event_message is not None:
            if "You`re to close to another airplane !" in event_message["message"] and "Correct your flight" in event_message["body"]:
                self.airplane.avoid_collision(50)
            elif "Crash !" in event_message["message"]:
                self.is_running = False

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            print("CLIENT`S UP...")
            client_socket.connect((HOST, PORT))
            self.selector.register(client_socket, selectors.EVENT_READ, data = None)
            welcome_message_from_server = self.initial_correspondence_with_server(client_socket)
            if welcome_message_from_server == None:
                self.stop(client_socket)
            else:
                initial_landing_point_coordinates = welcome_message_from_server["coordinates"]
                self.airplane.fly_to_initial_landing_point = True
                try:
                    while self.is_running:
                        self.events_service()
                        try:
                            fuel_reserves = self.airplane.fuel_consumption()
                            if not fuel_reserves:
                                self.send_message_to_server(client_socket, self.communication_utils.out_of_fuel_protocol())
                                self.stop(client_socket)
                            if self.airplane.fly_to_initial_landing_point:
                                distance = self.airplane.fly_to_target(initial_landing_point_coordinates)
                                self.send_airplane_coordinates(client_socket)
                                if distance < 100:
                                    self.send_message_to_server(client_socket, self.communication_utils.reaching_the_target_protocol("Initial landing point"))
                                    order_from_server_json = client_socket.recv(self.BUFFER)
                                    order_from_server = self.read_message_from_server(order_from_server_json)
                                    self.airplane.fly_to_initial_landing_point = False
                                    if f"Waiting point - {self.airplane.waiting_point}" in order_from_server["body"]:
                                        self.airplane.fly_to_waiting_point = True
                                        waiting_point_coordinates = order_from_server["coordinates"]
                                    elif f"Zero point - {self.airplane.zero_point}" in order_from_server["body"]:
                                        self.airplane.fly_to_runaway = True
                                        runaway_coordinates = order_from_server["coordinates"]
                            elif self.airplane.fly_to_waiting_point:
                                distance = self.airplane.fly_to_target(waiting_point_coordinates)
                                self.send_airplane_coordinates(client_socket)
                                if distance < 100:
                                    self.airplane.fly_to_waiting_point = False
                                    self.airplane.fly_to_initial_landing_point = True
                            elif self.airplane.fly_to_runaway:
                                distance = self.airplane.fly_to_target(runaway_coordinates)
                                self.send_airplane_coordinates(client_socket)
                                if distance < 50:
                                    self.send_message_to_server(client_socket, self.communication_utils.successfully_landing_protocol())
                                    self.is_running = False
                        except Exception as e:
                            print(f"Error: {e}")
                            self.is_running = False
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    self.stop(client_socket)

    def stop(self, client_socket):
        print("CLIENT`S OUT...")
        self.selector.close()
        client_socket.close()



if __name__ == "__main__":
    client = Client()
    client.start()
