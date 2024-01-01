import datetime
import socket as s
import threading
import schedule
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from communication_utils import ServerProtocols
from airport import Airport


class ConnectionPool:
    def __init__(self, min_numbers_of_connections, max_number_of_connections):
        self.connections_list = []
        self.connections_in_use_list = []
        self.lock = Lock()
        self.min_number_of_connections = min_numbers_of_connections
        self.max_number_of_connections = max_number_of_connections
        self.create_start_connections()
        self.connections_manager()

    def create_start_connections(self):
        for _ in range(self.min_number_of_connections):
            connection = ClientHandler(None, None)
            self.connections_list.append(connection)

    def get_connection(self, client_socket, address):
        self.lock.acquire()
        try:
            for connection in self.connections_list:
                if connection.in_use == False:
                    connection.in_use = True
                    connection.client_socket = client_socket
                    connection.address = address
                    self.connections_in_use_list.append(connection)
                    self.connections_list.remove(connection)
                    return connection
            if len(self.connections_list) < self.max_number_of_connections \
                    and len(self.connections_list) + len(self.connections_in_use_list) < self.max_number_of_connections:
                new_connection = ClientHandler(client_socket, address)
                new_connection.in_use = True
                self.connections_in_use_list.append(new_connection)
                return new_connection
            elif len(self.connections_list) + len(self.connections_in_use_list) >= self.max_number_of_connections:
                return False
        finally:
            self.lock.release()

    def release_connection(self, connection):
        self.lock.acquire()
        try:
            if connection in self.connections_in_use_list:
                connection.in_use = False
                connection.client_socket = None
                connection.address = None
                self.connections_in_use_list.remove(connection)
                self.connections_list.append(connection)
        finally:
            self.lock.release()

    def destroy_unused_connections(self):
        self.lock.acquire()
        try:
            for connection in self.connections_list:
                if len(self.connections_list) > 11:
                    connection.close()
                    self.connections_list.remove(connection)
                    if len(self.connections_list) == 10:
                        break
        except:
            self.lock.release()

    def keep_connections_at_the_starting_level(self):
        if len(self.connections_list) < self.min_number_of_connections:
            for _ in self.connections_list:
                connection = ClientHandler(None, None)
                self.connections_list.append(connection)
                if len(self.connections_list) == self.min_number_of_connections:
                    break

    def connections_manager(self):
        schedule.every(1).minute.do(self.destroy_unused_connections)
        schedule.every(1).minute.do(self.keep_connections_at_the_starting_level)


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address):
        super().__init__()
        self.server = Server()
        self.client_socket = client_socket
        self.address = address
        self.BUFFER = BUFFER
        self.data_utils = DataUtils()
        self.communication_utils = ServerProtocols()

    def run(self):
        welcome_message = self.communication_utils.welcome_protocol()
        self.server.send_message_to_client(self.client_socket, welcome_message)
        initial_coordinates_json = self.client_socket.recv(self.BUFFER)
        initial_coordinates = self.data_utils.deserialize_json(initial_coordinates_json)
        airplane = self.airport.create_airplane_object_and_append_it_to_list(initial_coordinates["body"])

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
        self.version = "0.2.1"
        self.communication_utils = ServerProtocols()
        self.server_connection = self.data_utils.create_connection()
        self.connection_pool = ConnectionPool(10, 100)
        self.airport = Airport()

    def send_message_to_client(self, client_socket, dict_data):
        message = self.data_utils.serialize_to_json(dict_data)
        client_socket.sendall(message)

    def close_client_socket_when_airplane_crashed_or_successfully_landed(self, airplane, client_socket):
        if airplane in self.airport.crashed_airplanes or airplane in self.airport.airplanes_with_successfully_landing:
            if airplane in self.airport.crashed_airplanes:
                crash_message = self.communication_utils.airplane_crashed()
                self.send_message_to_client(client_socket, crash_message)
            elif airplane in self.airport.airplanes_with_successfully_landing:
                landing_message = self.communication_utils.successfully_landing()
                self.send_message_to_client(client_socket, landing_message)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            print("Server`s up".upper())
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            while self.is_running:
                self.airport.airport_manager()
                client_socket, address = server_socket.accept()
                client_handler = self.connection_pool.get_connection(client_socket, address)
                client_handler.run()
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
