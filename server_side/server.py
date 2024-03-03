import datetime
import os
import socket as s
import threading
from threading import Lock
from config_variables_for_server_and_client import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, logger_config
from server_side.connection_pool import ConnectionPool
from server_side.database_and_serialization_managment import SerializeUtils, DatabaseUtils
from server_side.server_messages import ServerProtocols, HandlerProtocols
from server_side.airport import Airport, Radar


class ClientHandler(threading.Thread):
    """
    Handles communication with a single client_side connected to the server_side.

    Attributes:
        server: server_side whose manage this handler.
        client_socket (socket): The socket object representing the client_side connection.
        address (tuple): The address of the client_side (IP address, port number).
        thread_id (int): The unique identifier of the thread handling this client_side connection.
        connection (Connection): The database connection obtained from the connection pool.
        BUFFER (int): The size of the buffer used for sending and receiving data.
        serialize_utils (SerializeUtils): An instance of the SerializeUtils class for serialization.
        database_utils (DatabaseUtils): An instance of the DatabaseUtils class for database operations.
        communication_utils (HandlerProtocols): An instance of the HandlerProtocols class for communication protocols.
        is_running (bool): Flag indicating whether the client_side handler is running.
        airplane_object (dict): Dictionary representing the airplane object associated with the client_side.
        airplane_key (str): Key used to identify the airplane object in the dictionary.
    """

    def __init__(self, server, client_socket, address, thread_id):
        """
        Initializes a ClientHandler instance.

        Parameters:
            server: server_side whose manage client_side handlers.
            client_socket (socket): The socket object representing the client_side connection.
            address (tuple): The address of the client_side (IP address, port number).
            thread_id (int): The unique identifier of the thread handling this client_side connection.
        """
        super().__init__()
        self.server = server
        self.client_socket = client_socket
        self.address = address
        self.thread_id = thread_id
        self.connection = self.server.connection_pool.get_connection()
        self.BUFFER = BUFFER
        self.logger = logger_config(f"ClientHandler_{self.thread_id}", os.getcwd(), "server_logs.log")
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.communication_utils = HandlerProtocols()
        self.is_running = True
        self.airplane_object = None
        self.airplane_key = f"Airplane_{self.thread_id}"

    def send_message_to_client(self, data):
        """
        Sends a message to the client_side.

        Parameters:
            data (dict): The message data to be sent to the client_side.
        """
        message = self.serialize_utils.serialize_to_json(data)
        self.client_socket.sendall(message)

    def read_message_from_client(self, client_socket):
        """
        Reads a message from the client_side socket.

        Parameters:
            client_socket (socket): The client_side socket object from which to read the message.

        Returns:
            dict: The deserialized message received from the client_side.
        """
        message_from_client_json = client_socket.recv(self.BUFFER)
        deserialized_message = self.serialize_utils.deserialize_json(message_from_client_json)
        return deserialized_message

    def welcome_message(self, id):
        """
        Sends a welcome message to the client_side.

        Parameters:
            id (int): The identifier of the client_side.
        """
        welcome_message = self.communication_utils.welcome_message_to_client(id)
        self.logger.info(f"Client_{self.thread_id} connected")
        self.send_message_to_client(welcome_message)

    def response_from_client_with_coordinates(self):
        """
        Reads the coordinates message from the client_side and returns the coordinates.

        Returns:
            dict: The coordinates received from the client_side.
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
        quarter = self.server.airport.establish_airplane_quarter(coordinates)
        points_to_send = self.communication_utils.points_for_airplane_message(quarter,
                                                                              self.server.airport.initial_landing_point[quarter].point_coordinates(),
                                                                              self.server.airport.waiting_point[quarter].point_coordinates(),
                                                                              self.server.airport.zero_point[quarter[0]].point_coordinates())
        self.send_message_to_client(points_to_send)

    def initial_correspondence_with_client(self, client_socket):
        """
        Handles the initial correspondence with the client_side.
        Sends welcome message, obtains coordinates, establishes service points for the airplane,
        reads airplane object from client_side, and sends direction message to client_side.

        Parameters:
            client_socket (socket): The client_side socket object.
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
        possible_collisions = self.server.airport.check_distance_between_airplanes(self.airplane_object, self.airplane_key, self.server.airport.airplanes_list)
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
            response_from_client (dict): The response received from the client_side.
        """
        coordinates = [response_from_client["body"]["x"], response_from_client["body"]["y"], response_from_client["body"]["z"]]
        self.airplane_object[self.airplane_key]["coordinates"] = coordinates
        self.check_possible_collisions()
        self.server.airport.airplanes_list.update(self.airplane_object)

    def delete_airplane_from_list_and_save_status_to_db(self, status):
        """
        Deletes airplane from the list and updates its status in the database.

        Parameters:
            status (str): The status of the airplane.
        """
        self.database_utils.update_connection_status(self.connection, status, self.airplane_key)
        del self.server.airport.airplanes_list[self.airplane_key]
        self.is_running = False

    def handle_response_from_client(self, response_from_client):
        """
        Handles the response received from the client_side.
        Depending on the message received, it directs the airplane accordingly,
        updates its coordinates, or handles landing or crashing scenarios.

        Parameters:
            response_from_client (dict): The response received from the client_side.
        """
        air_corridor = getattr(self.server.airport, "air_corridor")[self.airplane_object[self.airplane_key]["quarter"][0]]
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
        Starts the client_side handler thread.
        Manages the communication with the client_side, handles responses, and manages the client_side's lifecycle.
        """
        self.initial_correspondence_with_client(self.client_socket)
        self.database_utils.add_new_connection_to_db(self.connection, self.airplane_key)
        self.server.airport.airplanes_list.update(self.airplane_object)
        try:
            while self.is_running:
                response_from_client = self.read_message_from_client(self.client_socket)
                self.handle_response_from_client(response_from_client)
        except Exception as e:
            self.logger.exception(f"Error in thread {self.thread_id}: {e}")
            self.is_running = False
        finally:
            self.stop()

    def stop(self):
        """
        Stops the client_side handler thread.
        Releases the connection, removes the client_side from the client_side list, and closes the client_side socket.
        """
        self.server.connection_pool.release_connection(self.connection)
        self.server.clients_list.remove(self)
        self.logger.info(f"Client {self.thread_id} out")
        self.client_socket.close()


class Server:
    """
    Represents the server_side handling the airport operations.

    Attributes:
        HOST (str): The host address.
        PORT (int): The port number.
        INTERNET_ADDRESS_FAMILY: The internet address family.
        SOCKET_TYPE: The socket type.
        logger: The logger object.
        serialize_utils (SerializeUtils): An instance of SerializeUtils for serialization.
        database_utils (DatabaseUtils): An instance of DatabaseUtils for database operations.
        lock (Lock): A lock for thread synchronization.
        is_running (bool): A flag indicating whether the server_side is running.
        start_date (datetime): The start date and time of the server_side.
        version (str): The version of the server_side.
        airport (Airport): An instance of the Airport class.
        communication_utils (ServerProtocols): An instance of ServerProtocols for communication protocols.
        connection_pool: Connection pool from which connections for server and handlers are taken
        server_connection: The server_side's database connection.
        clients_list (list): A list of connected clients.
    """

    def __init__(self, connection_pool):
        """
        Initializes the Server class with default values and objects.

        Parameters:
            - connection_pool: Connection pool object initialized before start the server_side.
        """
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.logger = logger_config("Server", r"C:\Programy\Python\Projekty\airport_project\server_side", "server_logs.log")
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "1.2.2"
        self.airport = Airport()
        self.communication_utils = ServerProtocols()
        self.connection_pool = connection_pool
        self.server_connection = self.connection_pool.get_connection()
        self.clients_list = []

    def check_server_lifetime(self):
        """
        Checks the server_side's lifetime to determine if it should stop running.
        """
        current_time = datetime.datetime.now()
        time_difference = current_time - self.start_date
        if time_difference >= datetime.timedelta(hours = 5):
            self.is_running = False

    def db_service_when_server_starts(self):
        """
        Performs database-related services when the server_side starts.
        This includes creating database tables and adding a new server_side period.
        """
        self.database_utils.create_db_tables(self.server_connection)
        self.database_utils.add_new_server_period(self.server_connection)

    def create_and_start_new_thread(self, client_socket, address):
        """
        Creates and starts a new thread to handle a client_side connection.

        Parameters:
            client_socket (socket): The client_side socket object.
            address (tuple): The client_side address.

        Returns:
            ClientHandler: The handler for the client_side connection.
        """
        thread_id = self.database_utils.get_all_airplanes_number_per_period(self.server_connection) + 1
        client_handler = ClientHandler(self, client_socket, address, thread_id)
        self.clients_list.append(client_handler)
        client_handler.start()
        return client_handler

    def handle_handler_exception(self, client_handler, error):
        """
        Handles exceptions raised in the client_side handler thread.

        Parameters:
            client_handler (ClientHandler): The client_side handler thread object.
            error (Exception): The exception raised.
        """
        self.logger.exception(f"Error in handler {client_handler.thread_id}: {error}")
        client_handler.stop()

    def handle_full_airport_situation(self, client_socket):
        """
        Handles the situation when the airport is full and rejects client_side connection.

        Parameters:
            client_socket (socket): The client_side socket object.
        """
        airport_full_message = self.communication_utils.airport_is_full_message()
        airport_full_message_json = self.serialize_utils.serialize_to_json(airport_full_message)
        client_socket.sendall(airport_full_message_json)
        client_socket.close()

    def handler_manager(self, client_socket, address):
        """
        Manages the creation of client_side handler threads and handles situations when the airport is full.

        Parameters:
            client_socket (socket): The client_side socket object.
            address (tuple): The client_side address.

        Returns:
            ClientHandler or None: The handler for the client_side connection if created, None otherwise.
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
        Manages the server_side's work, accepts client_side connections, and handles exceptions.

        Parameters:
            server_socket (socket): The server_side socket object.
        """
        try:
            self.check_server_lifetime()
            server_socket.settimeout(0.01)
            client_socket, address = server_socket.accept()
            self.logger.info(f"Connection from {address}")
            client_socket.settimeout(5)
            client_handler = self.handler_manager(client_socket, address)
        except s.timeout:
            pass
        except client_socket.timeout as e:
            self.handle_handler_exception(client_handler, e)

    def start(self):
        """
        Starts the server_side, initializes necessary services, and handles server_side operations.
        """
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            self.logger.info("Server`s up")
            self.db_service_when_server_starts()
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            try:
                while self.is_running:
                    radar.draw()
                    self.server_work_manager(server_socket)
            except OSError as e:
                self.logger.exception(f"Error in server_side: {e}")
                self.is_running = False
            finally:
                self.stop(server_socket)

    def stop(self, server_socket):
        """
        Stops the server_side, closes client_side connections, and performs cleanup operations.

        Parameters:
            server_socket (socket): The server_side socket object.
        """
        for handler in self.clients_list:
            handler.stop()
        self.database_utils.update_period_end(self.server_connection)
        self.logger.info("Server`s out")
        server_socket.close()



if __name__ == "__main__":
    connection_pool = ConnectionPool(10, 100)
    server = Server(connection_pool)
    radar = Radar(server.airport)
    server.start()
