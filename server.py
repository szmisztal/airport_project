import datetime
import logging
import socket as s
import threading
from threading import Lock
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER
from data_utils import DataUtils
from communication_utils import ServerProtocols
from airport import Airport
from connection_pool import ConnectionPool


logging.basicConfig(filename = "app.log", level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")


class ClientHandler(threading.Thread):
    def __init__(self, server, client_socket, address, thread_id):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.thread_id = thread_id
        self.connection = connection_pool.get_connection()
        self.BUFFER = BUFFER
        self.data_utils = DataUtils()
        self.communication_utils = ServerProtocols()
        self.is_running = True
        self.airport = server.airport
        self.airplane_object = None
        self.airplane_key = f"Airplane_{self.thread_id}"

    def send_message_to_client(self, data):
        message = self.data_utils.serialize_to_json(data)
        self.client_socket.sendall(message)

    def read_message_from_client(self, data):
        deserialized_data = self.data_utils.deserialize_json(data)
        return deserialized_data

    def welcome_message(self, id):
        welcome_message = self.communication_utils.welcome_protocol(id)
        self.send_message_to_client(welcome_message)

    def response_from_client_with_coordinates(self):
        coordinates_json = self.client_socket.recv(self.BUFFER)
        coordinates = self.data_utils.deserialize_json(coordinates_json)["body"]
        return coordinates

    def establish_all_service_points_for_airplane(self, coordinates):
        quarter = self.airport.establish_airplane_quarter(coordinates)
        points_for_airplane = {
            "quarter": quarter,
            "initial_landing_point": quarter,
            "waiting_point": quarter,
            "zero_point": quarter[0]
        }
        points_to_send = self.communication_utils.points_for_airplane_protocol(points_for_airplane)
        self.send_message_to_client(points_to_send)

    def direct_airplane_to_point(self, target, coordinates):
        direct_point = self.communication_utils.direct_airplane_protocol(target, coordinates)
        return self.send_message_to_client(direct_point)

    def return_point_coordinates(self, target, quarter):
        initial_landing_point_name = f"initial_landing_point_{quarter}"
        initial_landing_point = getattr(self.airport, initial_landing_point_name)
        waiting_point_name = f"waiting_point_for_landing_{quarter}"
        waiting_point = getattr(self.airport, waiting_point_name)
        zero_point_name = f"zero_point_{quarter[0]}"
        zero_point = getattr(self.airport, zero_point_name)
        if target == "initial landing point":
            return initial_landing_point.point_coordinates()
        elif target == "waiting point":
            return waiting_point.point_coordinates()
        elif target == "runaway":
            return zero_point.point_coordinates()

    def initial_correspondence_with_client(self):
        self.welcome_message(self.thread_id)
        coordinates = self.response_from_client_with_coordinates()
        self.establish_all_service_points_for_airplane(coordinates)
        airplane_object_json = self.client_socket.recv(self.BUFFER)
        airplane_object = self.read_message_from_client(airplane_object_json)
        self.airplane_object = airplane_object["body"]
        self.direct_airplane_to_point(f"Initial landing point - {self.airplane_object[self.airplane_key]['initial_landing_point']}",
                                      self.return_point_coordinates("initial landing point", self.airplane_object[self.airplane_key]["quarter"]))

    def check_possible_collisions(self):
        possible_collisions = server.airport.check_distance_between_airplanes(self.airplane_object, self.airplane_key, server.airport.airplanes_list)
        if possible_collisions == False:       # has to avoid collision
            self.send_message_to_client(self.communication_utils.avoid_collision_protocol())
        elif possible_collisions == None:      # airplanes crashed
            self.send_message_to_client(self.communication_utils.collision_protocol())
            self.data_utils.update_connection_status(self.connection, "CRASHED BY COLLISION", self.airplane_key)
            self.is_running = False
        else:                                  # everything` ok
            pass

    def run(self):
        self.initial_correspondence_with_client()
        self.data_utils.add_new_connection_to_db(self.connection, self.airplane_key)
        server.airport.airplanes_list.update(self.airplane_object)
        try:
            while self.is_running:
                response_from_client_json = self.client_socket.recv(self.BUFFER)
                response_from_client = self.data_utils.deserialize_json(response_from_client_json)
                if "We reached the target" in response_from_client["message"] and "Initial landing point" in response_from_client["body"]:
                    air_corridor_name = f"air_corridor_{self.airplane_object[self.airplane_key]['zero_point']}"
                    air_corridor = getattr(self.airport, air_corridor_name)
                    if air_corridor.occupied == True:
                        self.direct_airplane_to_point(f"Waiting point - {self.airplane_object[self.airplane_key]['waiting_point']}",
                                                      self.return_point_coordinates("waiting point", self.airplane_object[self.airplane_key]["quarter"]))
                    else:
                        self.direct_airplane_to_point(f"Zero point - {self.airplane_object[self.airplane_key]['zero_point']}",
                                  self.return_point_coordinates("runaway", self.airplane_object[self.airplane_key]["quarter"]))
                        air_corridor.occupied = True
                elif "Successfully landing" in response_from_client["message"] and "Goodbye !" in response_from_client["body"]:
                    air_corridor.occupied = False
                    self.data_utils.update_connection_status(self.connection, "SUCCESSFULLY LANDING", self.airplane_key)
                    self.is_running = False
                elif "Out of fuel !" in response_from_client["message"] and "We`re falling..." in response_from_client["body"]:
                    self.data_utils.update_connection_status(self.connection, "CRASHED BY OUT OF FUEL", self.airplane_key)
                    self.is_running = False
                else:
                    coordinates = [response_from_client["body"]["x"], response_from_client["body"]["y"], response_from_client["body"]["z"]]
                    self.airplane_object[self.airplane_key]["coordinates"] = coordinates
                    server.airport.airplanes_list.update(self.airplane_object)
                    print(server.airport.airplanes_list)
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
        self.data_utils = DataUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "0.9.3"
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
            self.data_utils.create_db_tables(self.server_connection)
            self.data_utils.add_new_server_period(self.server_connection)
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            try:
                while self.is_running:
                    try:
                        # self.airport.radar.draw_a_graph(self.clients_list)
                        server_lifetime = self.check_server_lifetime()
                        if not server_lifetime:
                            self.is_running = False
                        client_socket, address = server_socket.accept()
                        logger.info(f"Connection from {address}")
                        client_socket.settimeout(5)
                        print(self.airport.airplanes_list)
                        try:
                            self.lock.acquire()
                            if len(self.clients_list) < 100:
                                thread_id = self.data_utils.get_all_airplanes_number_per_period(self.server_connection)
                                client_handler = ClientHandler(self, client_socket, address, thread_id + 1)
                                self.clients_list.append(client_handler)
                                client_handler.start()
                            else:
                                airport_full_message = self.communication_utils.airport_full_protocol()
                                airport_full_message_json = self.data_utils.serialize_to_json(airport_full_message)
                                client_socket.sendall(airport_full_message_json)
                                client_socket.close()
                        except Exception as e:
                            logger.exception(f"Error in handler {thread_id}: {e}")
                            connection_pool.release_connection(client_handler.connection)
                            client_socket.close()
                            continue
                        finally:
                            self.lock.release()
                    except client_socket.timeout:
                        logger.debug(f"Client socket timeout in client {thread_id}")
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
        self.data_utils.update_period_end(self.server_connection)
        server_socket.close()



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    connection_pool = ConnectionPool(10, 100)
    server = Server()
    server.start()
