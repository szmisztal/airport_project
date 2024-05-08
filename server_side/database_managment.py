from sqlite3 import Error


class DatabaseUtils:
    """
    Utility class for executing SQL queries and managing database tables.
    """

    def execute_sql_query(self, connection, query, *args, fetch_option = None):
        """
        Execute an SQL query on the database.

        Parameters:
        - connection: Database connection object.
        - query (str): SQL query to be executed.
        - *args: Query parameters.
        - fetch_option (str): Option for fetching results ('fetchone' or 'fetchall').

        Returns:
        - Result of the query depending on the fetch_option.
        """
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

    def create_db_tables(self, connection):
        """
        Create database tables if they do not exist.

        Parameters:
        - connection: Database connection object.
        """
        self.create_server_periods_table(connection)
        self.create_connections_table(connection)

    def create_server_periods_table(self, connection):
        """
        Create the server_periods table if it does not exist.

        Parameters:
        - connection: Database connection object.
        """
        query = """CREATE TABLE IF NOT EXISTS server_periods(
                    period_id INTEGER PRIMARY KEY,
                    period_start DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    period_end DATETIME DEFAULT NULL
                    );"""
        self.execute_sql_query(connection, query)

    def create_connections_table(self, connection):
        """
        Create the connections table if it does not exist.

        Parameters:
        - connection: Database connection object.
        """
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
        """
        Adds a new server_side period to the database.

        Parameters:
        - connection: Database connection object.
        """
        query = "INSERT INTO server_periods DEFAULT VALUES"
        self.execute_sql_query(connection, query)

    def add_new_connection_to_db(self, connection, airplane_id):
        """
        Adds a new connection to the database.

        Parameters:
        - connection: Database connection object.
        - airplane_id: ID of the airplane to add to the database.
        """
        period_id = self.get_period_id(connection)
        query = "INSERT INTO connections (period_id, airplane_id) VALUES (?, ?)"
        self.execute_sql_query(connection, query, (period_id, airplane_id))

    def update_connection_status(self, connection, status, airplane_id):
        """
        Updates the status of a connection in the database.

        Parameters:
        - connection: Database connection object.
        - status: New status value.
        - airplane_id: ID of the airplane whose connection status is to be updated.
        """
        period_id = self.get_period_id(connection)
        query = "UPDATE connections SET status = ? WHERE connection_id = (SELECT connection_id FROM connections WHERE period_id = ? AND airplane_id = ?)"
        self.execute_sql_query(connection, query, (status, period_id, airplane_id))

    def update_period_end(self, connection):
        """
        Updates the end time of the current server_side period in the database.

        Parameters:
        - connection: Database connection object.
        """
        period_id = self.get_period_id(connection)
        query = "UPDATE server_periods SET period_end = CURRENT_TIMESTAMP WHERE period_id = ?"
        self.execute_sql_query(connection, query, (period_id, ))

    def get_period_id(self, connection):
        """
        Retrieves the ID of the current server_side period from the database.

        Parameters:
        - connection: Database connection object.

        Returns:
        - int: ID of the current server_side period.
        """
        period_id_query = "SELECT MAX(period_id) FROM server_periods"
        period_id = self.execute_sql_query(connection, period_id_query, fetch_option = "fetchone")[0]
        return int(period_id)

    def get_last_period_start_date(self, connection):
        """
        Retrieves the current server start from database.

        Parameters:
        - connection: Database connection object.

        Returns:
        - str: server start date in string type.
        """
        period_id = self.get_period_id(connection)
        query = "SELECT period_start FROM server_periods WHERE period_id = ?"
        period_start_date = self.execute_sql_query(connection, query, (period_id, ), fetch_option = "fetchone")[0]
        return period_start_date

    def get_airplanes_with_specified_status_per_period(self, connection, status):
        """
        Retrieves airplanes list with specified status - in the air, successfully landed or crashed

        Parameters:
        - connection: Database connection object.
        - status: string represents status (or None for NULL).

        Returns:
        - list: airplane_id with appearance time.
        """
        period_id = self.get_period_id(connection)
        query = "SELECT airplane_id, connection_date FROM connections WHERE period_id = ? AND (status = ? OR status IS NULL)"
        airplanes_with_status = self.execute_sql_query(connection, query, (period_id, status), fetch_option = "fetchall")
        return airplanes_with_status

    def get_single_airplane_details(self, connection, id):
        """
        Retrieves single airplane details.

        Parameters:
        - connection: Database connection object.
        - id: airplane id.

        Returns:
        - airplane_id, airplane_connection_date and status.
        """
        period_id = self.get_period_id(connection)
        query = "SELECT airplane_id, connection_date, status FROM connections WHERE period_id = ? AND airplane_id = ?"
        airplane_details = self.execute_sql_query(connection, query, (period_id, id), fetch_option = "fetchone")
        return airplane_details

    def get_all_airplanes_number_per_period(self, connection):
        """
        Retrieves the number of airplanes for the current period from the database.

        Parameters:
        - connection: Database connection object.

        Returns:
        - int: Number of airplanes for the current period.
        """
        period_id = self.get_period_id(connection)
        query = "SELECT * FROM connections WHERE period_id = ?"
        airplanes_list = self.execute_sql_query(connection, query, (period_id, ), fetch_option = "fetchall")
        if airplanes_list == None:
            return 0
        return len(airplanes_list)
