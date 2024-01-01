import json
import sqlite3
from sqlite3 import Error
from variables import encode_format


class DataUtils:
    def __init__(self, db_file = "airport_db.db"):
        self.db_file = db_file
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.in_use = False

    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
            try:
                self.cursor.execute(query, *args)
                self.connection.commit()
                if fetch_option == "fetchone":
                    return self.cursor.fetchone()
                elif fetch_option == "fetchall":
                    return self.cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                self.connection.rollback()
            finally:
                self.cursor.close()

    def create_connections_table(self):
        query = """CREATE TABLE IF NOT EXISTS connections(
                   connection_id INTEGER PRIMARY KEY,
                   connection_date DATE NOT NULL DEFAULT CURRENT_DATE,
                   airplane_id VARCHAR NOT NULL,
                   status VARCHAR DEFAULT NULL
                   );"""
        self.execute_sql_query(query)

    def add_new_connection_to_db(self, airplane):
        query = "INSERT INTO connections (airplane_id) VALUES (?)"
        self.execute_sql_query(query, (airplane, ))

    def update_status(self, status, airplane):
        query = "UPDATE connections SET status = ? WHERE connection_id = (SELECT connection_id FROM connections WHERE airplane_id = ?)"
        self.execute_sql_query(query, (status, str(airplane)))

    def get_all_airplanes_list(self):
        query = "SELECT * FROM connections"
        airplanes_list = self.execute_sql_query(query, fetch_option = "fetchall")
        if airplanes_list == None:
            return 0
        return len(airplanes_list)
