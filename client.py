import selectors
import socket as s
import time
import logging
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from database_and_serialization_managment import SerializeUtils
from airplane import Airplane
from server_client_messages import ClientProtocols


logging.basicConfig(filename = "clients_logs.log", level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")


class Client:
    """
    Represents a client for the airport simulation.

    Attributes:
    - HOST (str): The host address to connect to.
    - PORT (int): The port number to connect to.
    - INTERNET_ADDRESS_FAMILY (int): The internet address family (e.g., AF_INET for IPv4).
    - SOCKET_TYPE (int): The socket type (e.g., SOCK_STREAM for TCP).
    - BUFFER (int): The size of the buffer for receiving messages.
    - encode_format (str): The encoding format for messages.
    - selector (selectors.DefaultSelector): The selector for monitoring read events.
    - is_running (bool): Flag indicating whether the client is running.
    - communication_utils (ClientProtocols): Utility class for client-server communication.
    - airplane (Airplane): The airplane object associated with the client.
    """

    def __init__(self):
        """
        Initializes the Client object.
        """
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
        """
        Reads a message from the server.

        Parameters:
        - client_socket (socket): The client socket.

        Returns:
        - dict: The message received from the server.
        """
        message_from_server_json = client_socket.recv(self.BUFFER)
        deserialized_message = self.serialize_utils.deserialize_json(message_from_server_json)
        print(f">>> {deserialized_message['message']} {deserialized_message['body']}.")
        return deserialized_message

    def send_message_to_server(self, client_socket, data):
        """
        Sends a message to the server.

        Parameters:
        - client_socket (socket): The client socket.
        - data (dict): The data to be sent to the server.
        """
        client_request = self.serialize_utils.serialize_to_json(data)
        client_socket.sendall(client_request)

    def initial_correspondence_with_server(self, client_socket):
        """
        Handles the initial correspondence with the server.

        Parameters:
        - client_socket (socket): The client socket.
        """
        server_response = self.read_message_from_server(client_socket)
        if "Airport`s full: " in server_response["message"] and "You have to fly to another..." in server_response["body"]:
            self.stop(client_socket)
        else:
            self.airplane.id = server_response["id"]
            self.send_airplane_coordinates(client_socket, 0)
            self.establish_initial_airplane_points(client_socket)
            self.send_airplane_obj_to_server(client_socket)
            self.read_message_from_server(client_socket)
            self.airplane.fly_to_initial_landing_point = True

    def send_airplane_coordinates(self, client_socket, sleep_time_in_sec):
        """
        Sends the current coordinates of the airplane to the server.

        Parameters:
        - client_socket (socket): The client socket.
        """
        coordinates = self.communication_utils.airplane_coordinates_message(
            {"x": self.airplane.x,
             "y": self.airplane.y,
             "z": self.airplane.z}
        )
        self.send_message_to_server(client_socket, coordinates)
        time.sleep(sleep_time_in_sec)

    def establish_initial_airplane_points(self, client_socket):
        """
        Establishes the initial points of the airplane by reading data from the server.

        Parameters:
        - client_socket (socket): The client socket.
        """
        points = self.read_message_from_server(client_socket)
        self.airplane.set_points(points)

    def send_airplane_obj_to_server(self, client_socket):
        """
        Sends the airplane object to the server after converting it to a JSON format.

        Parameters:
        - client_socket (socket): The client socket.
        """
        airplane_obj = self.communication_utils.message_with_airplane_object(self.airplane.parse_airplane_obj_to_json())
        self.send_message_to_server(client_socket, airplane_obj)

    def check_additional_messages_from_server(self):
        """
        Checks for additional messages from the server.

        Returns:
        - dict or None: The message received from the server if available, otherwise None.
        """
        events = self.selector.select(timeout = 0)
        if events:
            for key, mask in events:
                if key.data is None:
                    server_message_json = key.fileobj.recv(self.BUFFER)
                    server_message = self.serialize_utils.deserialize_json(server_message_json)
                    print(f">>> {server_message['message']} {server_message['body']}.")
                    return server_message

    def handling_additional_messages_from_server(self, client_socket):
        """
        Handles additional messages received from the server.

        Parameters:
        - client_socket (socket): The client socket used for communication with the server.
        """
        event_message = self.check_additional_messages_from_server()
        if event_message is not None:
            if "You`re to close to another airplane !" in event_message["message"] and "Correct your flight" in event_message["body"]:
                self.airplane.avoid_collision(100)
            elif "Crash !" in event_message["message"] and "R.I.P." in event_message["body"]:
                self.send_message_to_server(client_socket, self.communication_utils.crash_message())
                self.is_running = False

    def start(self):
        """
        Starts the client by establishing a connection with the server and handling messages.

        This method sets up a socket connection with the server, registers the client socket
        with the selector for monitoring read events, and then starts the initial correspondence
        with the server. It continues handling additional messages and airplane movement until
        the client is stopped due to an OSError or automatically when the airplane lands safely,
        crashes due to a collision, or runs out of fuel.

        Raises:
        - OSError: If an error occurs during the execution of the client.
        """
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
        """
        Stops the client by closing the selector and client socket.

        This method closes the selector and client socket, effectively stopping the client's
        connection with the server.

        Parameters:
        - client_socket (socket): The client socket to be closed.
        """
        print("CLIENT`S OUT...")
        self.selector.close()
        client_socket.close()



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    client = Client()
    client.start()
