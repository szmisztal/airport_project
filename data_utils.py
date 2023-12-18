import json
from sqlite3 import Error
from variables import encode_format


class DataUtils:
    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def execute_sql_query(self, connection, query, *args, fetch_option = None):
            try:
                connection.cursor.execute(query, *args)
                connection.connection.commit()
                if fetch_option == "fetchone":
                    return connection.cursor.fetchone()
                elif fetch_option == "fetchall":
                    return connection.cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.connection.rollback()
            finally:
                if connection.cursor:
                    connection.cursor.close()

    def create_connections_table(self, connection):
        query = """CREATE TABLE IF NOT EXISTS connections(
                   connection_id INTEGER PRIMARY KEY,
                   connection_date DATE NOT NULL DEFAULT CURRENT_DATE,
                   airplane_id VARCHAR NOT NULL,
                   status VARCHAR DEFAULT NULL
                   );"""
        self.execute_sql_query(connection, query)

    def add_new_connection_to_db(self, connection, airplane):
        query = "INSERT INTO connections (airplane_id) VALUES (?)"
        self.execute_sql_query(connection, query, (airplane, ))

    def update_status(self, connection, status, airplane):
        query = "UPDATE connections SET status = ? WHERE connection_id = (SELECT connection_id FROM connections WHERE airplane_id = ?)"
        self.execute_sql_query(connection, query, (status, airplane))
