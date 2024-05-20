import datetime
import os
import socket as s
from threading import Lock
from common.config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, log_file
from common.logger_config import logger_config
from common.serialization_utils import SerializeUtils
from connection_pool import ConnectionPool
from database_managment import DatabaseUtils
from server_messages import ServerProtocols
from airport import Airport, Radar
from client_handler import ClientHandler


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
        self.server_socket = None
        self.logger = logger_config("Server", log_file, "server_logs.log")
        self.serialize_utils = SerializeUtils()
        self.database_utils = DatabaseUtils()
        self.lock = Lock()
        self.is_running = True
        self.start_date = datetime.datetime.now()
        self.version = "1.3.0"
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

    def check_file_flag_exists(self):
        """
        Checks that the flag file exists. If return True, the server will stop, if False, server will works normally.
        """
        path = f"{os.getcwd()}\\server_side\\flag_file.txt"
        file = os.path.isfile(path)
        return file

    def server_work_manager(self):
        """
        Manages the server_side's work, accepts client_side connections, and handles exceptions.
        """
        try:
            self.check_server_lifetime()
            self.server_socket.settimeout(0.01)
            client_socket, address = self.server_socket.accept()
            self.logger.info(f"Connection from {address}")
            client_socket.settimeout(5)
            client_handler = self.handler_manager(client_socket, address)
        except s.timeout:
            pass
        except client_socket.timeout as e:
            self.handle_handler_exception(client_handler, e)

    def main(self):
        """
        Starts the server_side, initializes necessary services, and handles server_side operations.
        """
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            self.server_socket = server_socket
            self.logger.info("Server`s up")
            self.db_service_when_server_starts()
            self.server_socket.bind((self.HOST, self.PORT))
            self.server_socket.listen()
            try:
                while self.is_running:
                    flag_file = self.check_file_flag_exists()
                    self.logger.info(flag_file)
                    if flag_file:
                        self.logger.info("Server paused")
                        continue
                    else:
                        radar.draw()
                        self.server_work_manager()
            except OSError as e:
                self.logger.exception(f"Error in server_side: {e}")
                self.is_running = False
            finally:
                self.stop()

    def stop(self):
        """
        Stops the server_side, closes client_side connections, and performs cleanup operations.
        """
        if len(self.clients_list) > 0:
            for handler in self.clients_list:
                handler.is_running = False
        self.database_utils.update_period_end(self.server_connection)
        self.logger.info("Server`s out")
        self.server_socket.close()



if __name__ == "__main__":
    connection_pool = ConnectionPool(10, 100)
    server = Server(connection_pool)
    radar = Radar(server.airport)
    server.main()
