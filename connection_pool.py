from threading import Lock
import schedule
import sqlite3
from sqlite3 import Error
from data_utils import SerializeUtils
from variables import db_file


class Connection:
    """
    Represents a database connection.

    Attributes:
    - db_file (str): The path to the SQLite database file.
    - connection: SQLite connection object.
    - cursor: Cursor object for executing SQL queries.
    - in_use (bool): Flag indicating whether the connection is in use.
    """

    def __init__(self):
        """
        Initializes a database connection.

        Parameters:
        - db_file (str): The path to the SQLite database file.
        """
        self.db_file = db_file
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.in_use = False

    def create_connection(self):
        """
        Creates a connection to the SQLite database.

        Returns:
        sqlite3.Connection or None: The connection object if successful, None otherwise.
        """
        try:
            with sqlite3.connect(self.db_file, check_same_thread = False) as connection:
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None


class ConnectionPool:
    """
    Manages a pool of database connections.

    Attributes:
    - connections_list (list): List of available connections.
    - connections_in_use_list (list): List of connections currently in use.
    - lock (threading.Lock): Lock for thread-safe access to the connection pool.
    - min_number_of_connections (int): Minimum number of connections to maintain.
    - max_number_of_connections (int): Maximum number of connections allowed in the pool.
    - serialize_utils (SerializeUtils): Utility for serialization.
    """

    def __init__(self, min_numbers_of_connections, max_number_of_connections):
        """
        Initializes the connection pool.

        Parameters:
        - min_number_of_connections (int): Minimum number of connections to maintain.
        - max_number_of_connections (int): Maximum number of connections allowed in the pool.
        """
        self.connections_list = []
        self.connections_in_use_list = []
        self.lock = Lock()
        self.min_number_of_connections = min_numbers_of_connections
        self.max_number_of_connections = max_number_of_connections
        self.create_start_connections()
        self.serialize_utils = SerializeUtils()
        self.connections_manager()

    def create_start_connections(self):
        """Creates the initial connections in the pool."""
        for _ in range(self.min_number_of_connections):
            connection = Connection()
            self.connections_list.append(connection)

    def get_connection(self):
        """
        Retrieves a connection from the pool.

        Returns:
        - Connection: A connection object if available, False otherwise.
        """
        with self.lock:
            for connection in self.connections_list:
                if connection.in_use == False:
                    connection.in_use = True
                    self.connections_in_use_list.append(connection)
                    self.connections_list.remove(connection)
                    return connection
            if len(self.connections_list) < self.max_number_of_connections \
                    and len(self.connections_list) + len(self.connections_in_use_list) < self.max_number_of_connections:
                new_connection = Connection()
                new_connection.in_use = True
                self.connections_in_use_list.append(new_connection)
                return new_connection
            elif len(self.connections_list) + len(self.connections_in_use_list) >= self.max_number_of_connections:
                return False

    def release_connection(self, connection):
        """
        Releases a connection back to the pool.

        Parameters:
        - connection (Connection): The connection to release.
        """
        with self.lock:
            if connection in self.connections_in_use_list:
                connection.in_use = False
                self.connections_list.append(connection)
                self.connections_in_use_list.remove(connection)

    def destroy_unused_connections(self):
        """Destroys unused connections in excess of the minimum number."""
        with self.lock:
            for connection in self.connections_list:
                if len(self.connections_list) >= 11:
                    connection.connection.close()
                    self.connections_list.remove(connection)
                    if len(self.connections_list) <= 10:
                        break

    def keep_connections_at_the_starting_level(self):
        """Ensures the connection pool maintains the minimum number of connections."""
        if len(self.connections_list) < self.min_number_of_connections:
            for _ in self.connections_list:
                connection = Connection()
                self.connections_list.append(connection)
                if len(self.connections_list) == self.min_number_of_connections:
                    break

    def connections_manager(self):
        """Manages connection pool tasks."""
        schedule.every(1).minute.do(self.keep_connections_at_the_starting_level)
        schedule.every(1).minute.do(self.destroy_unused_connections)
