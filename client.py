import selectors
import socket as s
import time
import logging
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import SerializeUtils
from airplane import Airplane
from communication_utils import ClientProtocols


logging.basicConfig(filename = "clients_logs.log", level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.selector = selectors.DefaultSelector()
        self.serialize_utils = SerializeUtils()
        self.is_running = True
        self.communication_utils = ClientProtocols()
        self.airplane = Airplane(self, Airplane.establish_init_airplane_coordinates())

    def read_message_from_server(self, client_socket):
        message_from_server_json = client_socket.recv(self.BUFFER)
        deserialized_message = self.serialize_utils.deserialize_json(message_from_server_json)
        print(f">>> {deserialized_message['message']} {deserialized_message['body']}.")
        return deserialized_message

    def send_message_to_server(self, client_socket, data):
        client_request = self.serialize_utils.serialize_to_json(data)
        client_socket.sendall(client_request)

    def initial_correspondence_with_server(self, client_socket):
        server_response = self.read_message_from_server(client_socket)
        if "Airport`s full: " in server_response["message"] and "You have to fly to another..." in server_response["body"]:
            self.stop(client_socket)
        else:
            self.airplane.id = server_response["id"]
            coordinates = self.communication_utils.airplane_coordinates_message(
                {"x": self.airplane.x,
                 "y": self.airplane.y,
                 "z": self.airplane.z}
            )
            self.send_message_to_server(client_socket, coordinates)
            points = self.read_message_from_server(client_socket)
            self.airplane.set_points(points)
            airplane_obj = self.communication_utils.message_with_airplane_object(self.airplane.parse_airplane_obj_to_json())
            self.send_message_to_server(client_socket, airplane_obj)
            self.read_message_from_server(client_socket)
            self.airplane.fly_to_initial_landing_point = True

    def send_airplane_coordinates(self, client_socket):
        coordinates = self.communication_utils.airplane_coordinates_message(
            {"x": self.airplane.x,
             "y": self.airplane.y,
             "z": self.airplane.z}
        )
        self.send_message_to_server(client_socket, coordinates)
        time.sleep(1)

    def check_additional_messages_from_server(self):
        events = self.selector.select(timeout = 0)
        if events:
            for key, mask in events:
                if key.data is None:
                    server_message_json = key.fileobj.recv(self.BUFFER)
                    server_message = self.serialize_utils.deserialize_json(server_message_json)
                    print(f">>> {server_message['message']} {server_message['body']}.")
                    return server_message

    def handling_additional_messages_from_server(self, client_socket):
        event_message = self.check_additional_messages_from_server()
        if event_message is not None:
            if "You`re to close to another airplane !" in event_message["message"] and "Correct your flight" in event_message["body"]:
                self.airplane.avoid_collision(100)
            elif "Crash !" in event_message["message"] and "R.I.P." in event_message["body"]:
                self.send_message_to_server(client_socket, self.communication_utils.crash_message())
                self.is_running = False

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            print("CLIENT`S UP...")
            client_socket.connect((HOST, PORT))
            self.selector.register(client_socket, selectors.EVENT_READ, data = None)
            try:
                self.initial_correspondence_with_server(client_socket)
                while self.is_running:
                    self.handling_additional_messages_from_server(client_socket)
                    self.airplane.airplane_movement_manager(client_socket)
            except OSError as e:
                logger.exception(f"Error: {e}")
                self.is_running = False
            finally:
                self.stop(client_socket)

    def stop(self, client_socket):
        print("CLIENT`S OUT...")
        self.selector.close()
        client_socket.close()



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    client = Client()
    client.start()
