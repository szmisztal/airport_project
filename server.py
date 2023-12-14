import socket as s
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from connection_pool import ConnectionPool
from communication_utils import ServerProtocols
from airport import Airport


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.data_utils = DataUtils()
        self.encode_format = encode_format
        self.is_running = True
        self.version = "0.0.8"
        self.communication_utils = ServerProtocols()
        self.connection_pool = ConnectionPool(10, 100)
        self.airport = Airport()

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            print("Server`s up")
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            with client_socket:
                connection = self.connection_pool.get_connection()
                welcome_message = self.data_utils.serialize_to_json(self.communication_utils.welcome_protocol())
                client_socket.sendall(welcome_message)
                initial_coordinates_json = client_socket.recv(self.BUFFER)
                initial_coordinates = self.data_utils.deserialize_json(initial_coordinates_json)
                self.airport.create_airplane_object_and_append_it_to_list(initial_coordinates)
                while self.is_running:
                    self.airport.airport_manager()




if __name__ == "__main__":
    server = Server()
    server.start()
