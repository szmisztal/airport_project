import datetime
import socket as s
import time
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from connection_pool import ConnectionPool, Connection
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
        self.start_date = datetime.datetime.now()
        self.version = "0.1.1"
        self.communication_utils = ServerProtocols()
        self.server_connection = Connection()
        self.connection_pool = ConnectionPool(10, 100)
        self.airport = Airport()

    def send_message_to_client(self, client_socket, dict_data):
        message = self.data_utils.serialize_to_json(dict_data)
        client_socket.sendall(message)

    def close_client_socket_when_airplane_crashed_or_successfully_landed(self, airplane, client_socket, connection):
        if airplane in self.airport.crashed_airplanes or airplane in self.airport.airplanes_with_successfully_landing:
            if airplane in self.airport.crashed_airplanes:
                crash_message = self.communication_utils.airplane_crashed()
                self.send_message_to_client(client_socket, crash_message)
                self.data_utils.update_status(connection, "Crashed", airplane)
            elif airplane in self.airport.airplanes_with_successfully_landing:
                landing_message = self.communication_utils.successfully_landing()
                self.send_message_to_client(client_socket, landing_message)
                self.data_utils.update_status(connection, "Landed", airplane)
            self.connection_pool.release_connection(connection)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            self.data_utils.create_connections_table(self.server_connection)
            print("Server`s up".upper())
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            with client_socket:
                connection = self.connection_pool.get_connection()
                if connection == False:
                    self.communication_utils.connections_limit()
                    client_socket.close()
                else:
                    welcome_message = self.communication_utils.welcome_protocol()
                    self.send_message_to_client(client_socket, welcome_message)
                    initial_coordinates_json = client_socket.recv(self.BUFFER)
                    initial_coordinates = self.data_utils.deserialize_json(initial_coordinates_json)
                    airplane = self.airport.create_airplane_object_and_append_it_to_list(initial_coordinates["body"])
                    self.data_utils.add_new_connection_to_db(connection, str(airplane))
                    while self.is_running:
                        self.airport.airport_manager()
                        print(airplane.x, airplane.y, airplane.z)
                        self.close_client_socket_when_airplane_crashed_or_successfully_landed(airplane, client_socket, connection)
                        time.sleep(1)
                        self.stop(server_socket)

    def stop(self, server_socket):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.start_date
        if time_difference >= datetime.timedelta(seconds = 3600):
            print("Server`s out...".upper())
            self.is_running = False
            server_socket.close()



if __name__ == "__main__":
    server = Server()
    server.start()
