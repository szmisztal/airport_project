import datetime
import logging
import socket as s
import threading
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER
from data_utils import SerializeUtils, DatabaseUtils
from communication_utils import ServerProtocols, HandlerProtocols
from airport import Airport, Radar
from connection_pool import ConnectionPool


logging.basicConfig(filename = "servers_logs.log", level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address, thread_id):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.thread_id = thread_id
        self.connection = connection_pool.get_connection()
        self.BUFFER = BUFFER
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.communication_utils = HandlerProtocols()
        self.is_running = True
        self.airplane_object = None
        self.airplane_key = f"Airplane_{self.thread_id}"

    def send_message_to_client(self, data):
        message = self.serialize_utils.serialize_to_json(data)
        self.client_socket.sendall(message)

    def read_message_from_client(self, client_socket):
        message_from_client_json = client_socket.recv(self.BUFFER)
        deserialized_message = self.serialize_utils.deserialize_json(message_from_client_json)
        return deserialized_message

    def welcome_message(self, id):
        welcome_message = self.communication_utils.welcome_message_to_client(id)
        self.send_message_to_client(welcome_message)

    def response_from_client_with_coordinates(self):
        coordinates_json = self.client_socket.recv(self.BUFFER)
        coordinates = self.serialize_utils.deserialize_json(coordinates_json)["body"]
        return coordinates

    def establish_all_service_points_coordinates_for_airplane(self, coordinates):
        quarter = server.airport.establish_airplane_quarter(coordinates)
        points_to_send = self.communication_utils.points_for_airplane_message(quarter,
                                                                              server.airport.initial_landing_point[quarter].point_coordinates(),
                                                                              server.airport.waiting_point[quarter].point_coordinates(),
                                                                              server.airport.zero_point[quarter[0]].point_coordinates())
        self.send_message_to_client(points_to_send)

    def initial_correspondence_with_client(self, client_socket):
        self.welcome_message(self.thread_id)
        coordinates = self.response_from_client_with_coordinates()
        self.establish_all_service_points_coordinates_for_airplane(coordinates)
        airplane_object = self.read_message_from_client(client_socket)
        self.airplane_object = airplane_object["body"]
        self.send_message_to_client(self.communication_utils.direct_airplane_message("Initial landing point"))

    def check_possible_collisions(self):
        possible_collisions = server.airport.check_distance_between_airplanes(self.airplane_object, self.airplane_key, server.airport.airplanes_list)
        if possible_collisions == False:       # has to avoid collision
            self.send_message_to_client(self.communication_utils.avoid_collision_message())
        elif possible_collisions == None:      # airplanes crashed
            self.send_message_to_client(self.communication_utils.collision_message())
        else:                                  # everything` ok
            pass

    def delete_airplane_from_list_and_save_status_to_db(self, status):
        self.database_utils.update_connection_status(self.connection, status, self.airplane_key)
        del server.airport.airplanes_list[self.airplane_key]
        self.is_running = False

    def run(self):
        self.initial_correspondence_with_client(self.client_socket)
        self.database_utils.add_new_connection_to_db(self.connection, self.airplane_key)
        server.airport.airplanes_list.update(self.airplane_object)
        try:
            while self.is_running:
                response_from_client = self.read_message_from_client(self.client_socket)
                if "We reached the target: " in response_from_client["message"] and "Initial landing point" in response_from_client["body"]:
                    air_corridor = getattr(server.airport, "air_corridor")[self.airplane_object[self.airplane_key]["quarter"][0]]
                    if air_corridor.occupied == True:
                        self.send_message_to_client(self.communication_utils.direct_airplane_message("Waiting point"))
                    else:
                        self.send_message_to_client(self.communication_utils.direct_airplane_message("Zero point"))
                        air_corridor.occupied = True
                elif "Successfully landing" in response_from_client["message"] and "Goodbye !" in response_from_client["body"]:
                    air_corridor.occupied = False
                    self.delete_airplane_from_list_and_save_status_to_db("SUCCESSFULLY LANDING")
                elif "Out of fuel !" in response_from_client["message"] and "We`re falling..." in response_from_client["body"]:
                    self.delete_airplane_from_list_and_save_status_to_db("CRASHED BY OUT OF FUEL")
                elif "Crash !" in response_from_client["message"] and "Bye, bye..." in response_from_client["body"]:
                    self.delete_airplane_from_list_and_save_status_to_db("CRASHED BY COLLISION")
                else:
                    coordinates = [response_from_client["body"]["x"], response_from_client["body"]["y"], response_from_client["body"]["z"]]
                    self.airplane_object[self.airplane_key]["coordinates"] = coordinates
                    self.check_possible_collisions()
                    server.airport.airplanes_list.update(self.airplane_object)
        except Exception as e:
            logger.exception(f"Error in thread {self.thread_id}: {e}")
            self.is_running = False
        finally:
            self.stop()

    def stop(self):
        print(f"CLIENT: {self.thread_id} IS OUT...")
        connection_pool.release_connection(self.connection)
        server.clients_list.remove(self)
        logger.info(f"Client {self.thread_id} out")
        self.client_socket.close()


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "1.1.0"
        self.airport = Airport()
        self.communication_utils = ServerProtocols()
        self.server_connection = connection_pool.get_connection()
        self.clients_list = []

    def check_server_lifetime(self):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.start_date
        if time_difference >= datetime.timedelta(seconds = 3600):
            return False
        else:
            return True

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            print("SERVER`S UP...")
            self.database_utils.create_db_tables(self.server_connection)
            self.database_utils.add_new_server_period(self.server_connection)
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            try:
                while self.is_running:
                    try:
                        server_socket.settimeout(0.01)
                        radar.draw()
                        server_lifetime = self.check_server_lifetime()
                        if not server_lifetime:
                            self.is_running = False
                        client_socket, address = server_socket.accept()
                        logger.info(f"Connection from {address}")
                        client_socket.settimeout(5)
                        try:
                            self.lock.acquire()
                            if len(self.clients_list) < 100:
                                thread_id = self.database_utils.get_all_airplanes_number_per_period(self.server_connection)
                                client_handler = ClientHandler(client_socket, address, thread_id + 1)
                                self.clients_list.append(client_handler)
                                client_handler.start()
                            else:
                                airport_full_message = self.communication_utils.airport_is_full_message()
                                airport_full_message_json = self.serialize_utils.serialize_to_json(airport_full_message)
                                client_socket.sendall(airport_full_message_json)
                                client_socket.close()
                        except Exception as e:
                            logger.exception(f"Error in handler {thread_id}: {e}")
                            connection_pool.release_connection(client_handler.connection)
                            client_socket.close()
                            continue
                        finally:
                            self.lock.release()
                    except s.timeout:
                        pass
                    except client_socket.timeout:
                        logger.exception(f"Client socket timeout in client {thread_id}")
                        connection_pool.release_connection(client_handler.connection)
                        client_socket.close()
                        continue
            except Exception as e:
                logger.exception(f"Error in server: {e}")
                self.is_running = False
            finally:
                self.stop(server_socket)

    def stop(self, server_socket):
        print("SERVER`S OUT...")
        for client in self.clients_list:
            connection_pool.release_connection(client.connection)
            client.client_socket.close()
        self.database_utils.update_period_end(self.server_connection)
        logger.info("Server`s out")
        server_socket.close()



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    connection_pool = ConnectionPool(10, 100)
    server = Server()
    radar = Radar(server.airport)
    server.start()
