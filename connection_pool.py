from threading import Lock
import schedule
import sqlite3
from sqlite3 import Error
from data_utils import SerializeUtils
from variables import db_file


class Connection:
    def __init__(self):
        self.db_file = db_file
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.in_use = False

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file, check_same_thread = False)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None


class ConnectionPool:
    def __init__(self, min_numbers_of_connections, max_number_of_connections):
        self.connections_list = []
        self.connections_in_use_list = []
        self.lock = Lock()
        self.min_number_of_connections = min_numbers_of_connections
        self.max_number_of_connections = max_number_of_connections
        self.create_start_connections()
        self.serialize_utils = SerializeUtils()
        self.connections_manager()

    def create_start_connections(self):
        for _ in range(self.min_number_of_connections):
            connection = Connection()
            self.connections_list.append(connection)

    def get_connection(self):
        self.lock.acquire()
        try:
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
        finally:
            self.lock.release()

    def release_connection(self, connection):
        self.lock.acquire()
        try:
            if connection in self.connections_in_use_list:
                connection.in_use = False
                self.connections_list.append(connection)
                self.connections_in_use_list.remove(connection)
        finally:
            self.lock.release()

    def destroy_unused_connections(self):
        self.lock.acquire()
        try:
            for connection in self.connections_list:
                if len(self.connections_list) > 11:
                    connection.close()
                    self.connections_list.remove(connection)
                    if len(self.connections_list) <= 10:
                        break
        finally:
            self.lock.release()

    def keep_connections_at_the_starting_level(self):
        if len(self.connections_list) < self.min_number_of_connections:
            for _ in self.connections_list:
                connection = Connection()
                self.connections_list.append(connection)
                if len(self.connections_list) == self.min_number_of_connections:
                    break

    def connections_manager(self):
        schedule.every(1).minute.do(self.keep_connections_at_the_starting_level)
        schedule.every(1).minute.do(self.destroy_unused_connections)
