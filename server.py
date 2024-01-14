import datetime
import socket as s
import threading
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER
from data_utils import DataUtils
from communication_utils import ServerProtocols
from airport import Airport
from connection_pool import ConnectionPool


class ClientHandler(threading.Thread):
    def __init__(self, server, client_socket, address, thread_id, connection):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.thread_id = thread_id
        self.connection = connection
        self.BUFFER = BUFFER
        self.data_utils = DataUtils()
        self.communication_utils = ServerProtocols()
        self.is_running = True
        self.airport = server.airport
        self.airplane_x = None
        self.airplane_y = None
        self.airplane_z = None
        self.airplane_quarter = None

    def send_message_to_client(self, dict_data):
        message = self.data_utils.serialize_to_json(dict_data)
        self.client_socket.sendall(message)

    def welcome_message(self, id):
        welcome_message = self.communication_utils.welcome_protocol(id)
        self.send_message_to_client(welcome_message)

    def response_from_client_with_coordinates(self):
        coordinates_json = self.client_socket.recv(self.BUFFER)
        coordinates = self.data_utils.deserialize_json(coordinates_json)["body"]
        return coordinates

    def run(self):
        self.welcome_message(self.thread_id)
        while self.is_running:
            coordinates_json = self.client_socket.recv(BUFFER)
            coordinates = self.data_utils.deserialize_json(coordinates_json)
            self.airplane_x, self.airplane_y, self.airplane_z, self.airplane_quarter = \
                coordinates["body"]["x"], coordinates["body"]["y"], coordinates["body"]["z"], coordinates["body"]["quarter"]


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.data_utils = DataUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "0.5.2"
        self.airport = Airport()
        self.connection_pool = ConnectionPool(10, 100)
        self.server_connection = self.connection_pool.get_connection()
        self.clients_list = []

    # def close_client_socket_when_airplane_crashed_or_successfully_landed(self, airplane, client_socket):
    #     if airplane in self.airport.crashed_airplanes or airplane in self.airport.airplanes_with_successfully_landing:
    #         if airplane in self.airport.crashed_airplanes:
    #             crash_message = self.communication_utils.airplane_crashed()
    #             self.send_message_to_client(client_socket, crash_message)
    #         elif airplane in self.airport.airplanes_with_successfully_landing:
    #             landing_message = self.communication_utils.successfully_landing()
    #             self.send_message_to_client(client_socket, landing_message)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            print("SERVER`S UP...")
            self.data_utils.create_connections_table(self.server_connection)
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            try:
                while self.is_running:
                    server_lifetime = self.check_server_lifetime()
                    if not server_lifetime:
                        self.stop(server_socket)
                    else:
                        if len(self.clients_list) > 0:
                            self.airport.airport_manager(self.clients_list)
                        else:
                            print("Waiting for airplanes...")
                    server_socket.settimeout(1)
                    try:
                        client_socket, address = server_socket.accept()
                        try:
                            self.lock.acquire()
                            thread_id = self.data_utils.get_all_airplanes_list(self.server_connection)
                            client_handler = ClientHandler(self, client_socket, address, thread_id + 1,
                                                           self.connection_pool.get_connection())
                            self.clients_list.append(client_handler)
                            client_handler.start()
                            client_handler.run()
                        except Exception as e:
                            print(f"Error: {e}")
                            pass  # add exception service
                        finally:
                            self.lock.release()
                    except server_socket.timeout:
                        continue
            except Exception as e:
                print(f"Error: {e}")
                pass  # add exception service
            finally:
                server_socket.close()

    def check_server_lifetime(self):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.start_date
        if time_difference >= datetime.timedelta(seconds = 3600):
            return False
        else:
            return True

    def stop(self, server_socket):
        print("SERVER`S OUT...")
        self.is_running = False
        server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start()
