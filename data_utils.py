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
            else:
                return None
        except Error as e:
            print(f"Error: {e}")
            connection.connection.rollback()
            return None

    def create_db_tables(self, connection):
        self.create_server_periods_table(connection)
        self.create_connections_table(connection)

    def create_server_periods_table(self, connection):
        query = """CREATE TABLE IF NOT EXISTS server_periods(
                    period_id INTEGER PRIMARY KEY,
                    period_start DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    period_end DATETIME DEFAULT NULL
                    );"""
        self.execute_sql_query(connection, query)

    def create_connections_table(self, connection):
        query = """CREATE TABLE IF NOT EXISTS connections(
                   connection_id INTEGER PRIMARY KEY,
                   period_id INTEGER NOT NULL,
                   connection_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   airplane_id VARCHAR NOT NULL,
                   status VARCHAR DEFAULT NULL,
                   FOREIGN KEY (period_id) REFERENCES server_periods (period_id) ON DELETE CASCADE
                   );"""
        self.execute_sql_query(connection, query)

    def add_new_server_period(self, connection):
        query = "INSERT INTO server_periods DEFAULT VALUES"
        self.execute_sql_query(connection, query)

    def add_new_connection_to_db(self, connection, airplane_id):
        period_id = self.get_period_id(connection)
        query = "INSERT INTO connections (period_id, airplane_id) VALUES (?, ?)"
        self.execute_sql_query(connection, query, (period_id, airplane_id))

    def update_connection_status(self, connection, status, airplane_id):
        period_id = self.get_period_id(connection)
        query = "UPDATE connections SET status = ? WHERE connection_id = (SELECT connection_id FROM connections WHERE period_id = ? AND airplane_id = ?)"
        self.execute_sql_query(connection, query, (status, period_id, airplane_id))

    def update_period_end(self, connection):
        period_id = self.get_period_id(connection)
        query = "UPDATE server_periods SET period_end = CURRENT_TIMESTAMP WHERE period_id = ?"
        self.execute_sql_query(connection, query, (period_id, ))

    def get_period_id(self, connection):
        period_id_query = "SELECT MAX(period_id) FROM server_periods"
        period_id = self.execute_sql_query(connection, period_id_query, fetch_option = "fetchone")[0]
        return int(period_id)

    def get_all_airplanes_number_per_period(self, connection):
        period_id = self.get_period_id(connection)
        query = "SELECT * FROM connections WHERE period_id = ?"
        airplanes_list = self.execute_sql_query(connection, query, (period_id, ), fetch_option = "fetchall")
        if airplanes_list == None:
            return 0
        return len(airplanes_list)
