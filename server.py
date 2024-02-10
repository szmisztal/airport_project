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
    """
    Handles communication with a single client connected to the server.

    Attributes:
        client_socket (socket): The socket object representing the client connection.
        address (tuple): The address of the client (IP address, port number).
        thread_id (int): The unique identifier of the thread handling this client connection.
        connection (Connection): The database connection obtained from the connection pool.
        BUFFER (int): The size of the buffer used for sending and receiving data.
        serialize_utils (SerializeUtils): An instance of the SerializeUtils class for serialization.
        database_utils (DatabaseUtils): An instance of the DatabaseUtils class for database operations.
        communication_utils (HandlerProtocols): An instance of the HandlerProtocols class for communication protocols.
        is_running (bool): Flag indicating whether the client handler is running.
        airplane_object (dict): Dictionary representing the airplane object associated with the client.
        airplane_key (str): Key used to identify the airplane object in the dictionary.
    """

    def __init__(self, client_socket, address, thread_id):
        """
        Initializes a ClientHandler instance.

        Parameters:
            client_socket (socket): The socket object representing the client connection.
            address (tuple): The address of the client (IP address, port number).
            thread_id (int): The unique identifier of the thread handling this client connection.
        """
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
        """
        Sends a message to the client.

        Parameters:
            data (dict): The message data to be sent to the client.
        """
        message = self.serialize_utils.serialize_to_json(data)
        self.client_socket.sendall(message)

    def read_message_from_client(self, client_socket):
        """
        Reads a message from the client socket.

        Parameters:
            client_socket (socket): The client socket object from which to read the message.

        Returns:
            dict: The deserialized message received from the client.
        """
        message_from_client_json = client_socket.recv(self.BUFFER)
        deserialized_message = self.serialize_utils.deserialize_json(message_from_client_json)
        return deserialized_message

    def welcome_message(self, id):
        """
        Sends a welcome message to the client.

        Parameters:
            id (int): The identifier of the client.
        """
        welcome_message = self.communication_utils.welcome_message_to_client(id)
        self.send_message_to_client(welcome_message)

    def response_from_client_with_coordinates(self):
        """
        Reads the coordinates message from the client and returns the coordinates.

        Returns:
            dict: The coordinates received from the client.
        """
        coordinates_json = self.client_socket.recv(self.BUFFER)
        coordinates = self.serialize_utils.deserialize_json(coordinates_json)["body"]
        return coordinates

    def establish_all_service_points_coordinates_for_airplane(self, coordinates):
        """
        Sends all service points' coordinates for the airplane based on the provided coordinates.

        Parameters:
            coordinates (dict): The coordinates of the airplane.
        """
        quarter = server.airport.establish_airplane_quarter(coordinates)
        points_to_send = self.communication_utils.points_for_airplane_message(quarter,
                                                                              server.airport.initial_landing_point[quarter].point_coordinates(),
                                                                              server.airport.waiting_point[quarter].point_coordinates(),
                                                                              server.airport.zero_point[quarter[0]].point_coordinates())
        self.send_message_to_client(points_to_send)

    def initial_correspondence_with_client(self, client_socket):
        """
        Handles the initial correspondence with the client.
        Sends welcome message, obtains coordinates, establishes service points for the airplane,
        reads airplane object from client, and sends direction message to client.

        Parameters:
            client_socket (socket): The client socket object.
        """
        self.welcome_message(self.thread_id)
        coordinates = self.response_from_client_with_coordinates()
        self.establish_all_service_points_coordinates_for_airplane(coordinates)
        airplane_object = self.read_message_from_client(client_socket)
        self.airplane_object = airplane_object["body"]
        self.send_message_to_client(self.communication_utils.direct_airplane_message("Initial landing point"))

    def check_possible_collisions(self):
        """
        Checks for possible collisions between airplanes.
        Sends messages accordingly if there's a collision or if avoidance is necessary.
        """
        possible_collisions = server.airport.check_distance_between_airplanes(self.airplane_object, self.airplane_key, server.airport.airplanes_list)
        if possible_collisions == False:
            self.send_message_to_client(self.communication_utils.avoid_collision_message())
        elif possible_collisions == None:
            self.send_message_to_client(self.communication_utils.collision_message())
        else:
            pass

    def update_airplane_coordinates(self, response_from_client):
        """
        Updates the coordinates of the airplane object and checks for collisions.

        Parameters:
            response_from_client (dict): The response received from the client.
        """
        coordinates = [response_from_client["body"]["x"], response_from_client["body"]["y"], response_from_client["body"]["z"]]
        self.airplane_object[self.airplane_key]["coordinates"] = coordinates
        self.check_possible_collisions()
        server.airport.airplanes_list.update(self.airplane_object)

    def delete_airplane_from_list_and_save_status_to_db(self, status):
        """
        Deletes airplane from the list and updates its status in the database.

        Parameters:
            status (str): The status of the airplane.
        """
        self.database_utils.update_connection_status(self.connection, status, self.airplane_key)
        del server.airport.airplanes_list[self.airplane_key]
        self.is_running = False

    def handle_response_from_client(self, response_from_client):
        """
        Handles the response received from the client.
        Depending on the message received, it directs the airplane accordingly,
        updates its coordinates, or handles landing or crashing scenarios.

        Parameters:
            response_from_client (dict): The response received from the client.
        """
        air_corridor = getattr(server.airport, "air_corridor")[self.airplane_object[self.airplane_key]["quarter"][0]]
        if "We reached the target: " in response_from_client["message"] and "Initial landing point" in response_from_client["body"]:
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
            self.update_airplane_coordinates(response_from_client)

    def run(self):
        """
        Starts the client handler thread.
        Manages the communication with the client, handles responses, and manages the client's lifecycle.
        """
        self.initial_correspondence_with_client(self.client_socket)
        self.database_utils.add_new_connection_to_db(self.connection, self.airplane_key)
        server.airport.airplanes_list.update(self.airplane_object)
        try:
            while self.is_running:
                response_from_client = self.read_message_from_client(self.client_socket)
                self.handle_response_from_client(response_from_client)
        except Exception as e:
            logger.exception(f"Error in thread {self.thread_id}: {e}")
            self.is_running = False
        finally:
            self.stop()

    def stop(self):
        """
        Stops the client handler thread.
        Releases the connection, removes the client from the client list, and closes the client socket.
        """
        print(f"CLIENT: {self.thread_id} IS OUT...")
        connection_pool.release_connection(self.connection)
        server.clients_list.remove(self)
        logger.info(f"Client {self.thread_id} out")
        self.client_socket.close()


class Server:
    """
    Represents the server handling the airport operations.

    Attributes:
        HOST (str): The host address.
        PORT (int): The port number.
        INTERNET_ADDRESS_FAMILY: The internet address family.
        SOCKET_TYPE: The socket type.
        serialize_utils (SerializeUtils): An instance of SerializeUtils for serialization.
        database_utils (DatabaseUtils): An instance of DatabaseUtils for database operations.
        lock (Lock): A lock for thread synchronization.
        is_running (bool): A flag indicating whether the server is running.
        start_date (datetime): The start date and time of the server.
        version (str): The version of the server.
        airport (Airport): An instance of the Airport class.
        communication_utils (ServerProtocols): An instance of ServerProtocols for communication protocols.
        server_connection: The server's database connection.
        clients_list (list): A list of connected clients.
    """

    def __init__(self):
        """
        Initializes the Server class with default values and objects.
        """
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "1.2.0"
        self.airport = Airport()
        self.communication_utils = ServerProtocols()
        self.server_connection = connection_pool.get_connection()
        self.clients_list = []

    def check_server_lifetime(self):
        """
        Checks the server's lifetime to determine if it should stop running.
        """
        current_time = datetime.datetime.now()
        time_difference = current_time - self.start_date
        if time_difference >= datetime.timedelta(seconds = 3600):
            self.is_running = False

    def db_service_when_server_starts(self):
        """
        Performs database-related services when the server starts.
        This includes creating database tables and adding a new server period.
        """
        self.database_utils.create_db_tables(self.server_connection)
        self.database_utils.add_new_server_period(self.server_connection)

    def create_and_start_new_thread(self, client_socket, address):
        """
        Creates and starts a new thread to handle a client connection.

        Args:
            client_socket (socket): The client socket object.
            address (tuple): The client address.

        Returns:
            ClientHandler: The handler for the client connection.
        """
        thread_id = self.database_utils.get_all_airplanes_number_per_period(self.server_connection) + 1
        client_handler = ClientHandler(client_socket, address, thread_id)
        self.clients_list.append(client_handler)
        client_handler.start()
        return client_handler

    def handle_handler_exception(self, client_handler, error):
        """
        Handles exceptions raised in the client handler thread.

        Args:
            client_handler (ClientHandler): The client handler thread object.
            error (Exception): The exception raised.
        """
        logger.exception(f"Error in handler {client_handler.thread_id}: {error}")
        client_handler.stop()

    def handle_full_airport_situation(self, client_socket):
        """
        Handles the situation when the airport is full and rejects client connection.

        Parameters:
            client_socket (socket): The client socket object.
        """
        airport_full_message = self.communication_utils.airport_is_full_message()
        airport_full_message_json = self.serialize_utils.serialize_to_json(airport_full_message)
        client_socket.sendall(airport_full_message_json)
        client_socket.close()

    def handler_manager(self, client_socket, address):
        """
        Manages the creation of client handler threads and handles situations when the airport is full.

        Parameters:
            client_socket (socket): The client socket object.
            address (tuple): The client address.

        Returns:
            ClientHandler or None: The handler for the client connection if created, None otherwise.
        """
        try:
            with self.lock:
                if len(self.clients_list) < 100:
                    client_handler = self.create_and_start_new_thread(client_socket, address)
                    return client_handler
                else:
                    self.handle_full_airport_situation(client_socket)
        except OSError as e:
            self.handle_handler_exception(client_handler, e)

    def server_work_manager(self, server_socket):
        """
        Manages the server's work, accepts client connections, and handles exceptions.

        Parameters:
            server_socket (socket): The server socket object.
        """
        try:
            self.check_server_lifetime()
            server_socket.settimeout(0.01)
            radar.draw()
            client_socket, address = server_socket.accept()
            logger.info(f"Connection from {address}")
            client_socket.settimeout(5)
            client_handler = self.handler_manager(client_socket, address)
        except s.timeout:
            pass
        except client_socket.timeout as e:
            self.handle_handler_exception(client_handler, e)

    def start(self):
        """
        Starts the server, initializes necessary services, and handles server operations.
        """
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            print("SERVER`S UP...")
            self.db_service_when_server_starts()
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            try:
                while self.is_running:
                    self.server_work_manager(server_socket)
            except OSError as e:
                logger.exception(f"Error in server: {e}")
                self.is_running = False
            finally:
                self.stop(server_socket)

    def stop(self, server_socket):
        """
        Stops the server, closes client connections, and performs cleanup operations.

        Parameters:
            server_socket (socket): The server socket object.
        """
        print("SERVER`S OUT...")
        for handler in self.clients_list:
            handler.stop()
        self.database_utils.update_period_end(self.server_connection)
        logger.info("Server`s out")
        server_socket.close()



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    connection_pool = ConnectionPool(10, 100)
    server = Server()
    radar = Radar(server.airport)
    server.start()
