import os
import subprocess
import datetime as dt
import requests
from jsonrpcserver import method, serve
from config_variables_for_server_and_client import logger_config, db_file
from server_side.connection_pool import Connection
from server_side.database_and_serialization_managment import DatabaseUtils


class API:
    """
    A class to control and interact with a server that processes and manages airplane data.

    Attributes:
        is_running (bool): Flag indicating whether the server is running.
        logger (Logger): Logger object to log information and errors.
        connection (Connection): Connection object to interact with the database.
        db_utils (DatabaseUtils): Utility object for database operations.
        process (subprocess.Popen): Represents the running server process.
    """

    def __init__(self):
        """
        Initializes the API class with default values and configurations.
        """
        self.is_running = False
        self.logger = logger_config("API logger", os.getcwd(), "api_logs.log")
        self.connection = Connection(db_file)
        self.db_utils = DatabaseUtils()
        self.process = None

    @method
    def server_start(self):
        """
        Starts the server script as a subprocess and updates the API state.

        Returns:
            subprocess.Popen: The subprocess object for the running server.
        """
        server_script_path = f"{os.getcwd()}/server_side/server.py"
        self.process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        self.is_running = True
        self.logger.info(f"Started script with PID {self.process.pid}")
        return self.process

    def server_close(self):
        """
        Terminates the server subprocess, updates the database, and closes the database connection.

        Returns:
            dict: A response message indicating the server has stopped.
        """
        self.process.terminate()
        self.process.wait()
        self.logger.info(f"Close script with PID {self.process.pid}")
        self.process = None
        self.db_utils.update_period_end(self.connection)
        self.connection.connection.close()
        return {"message": "Server stopped"}

    def server_pause(self):
        """
        Creates a flag file to signal the server to pause its operations.

        Returns:
            dict: A response indicating the server's paused status.
        """
        path = f"{os.getcwd()}\\server_side\\flag_file.txt"
        with open(path, "w"):
            pass
        return {"server status": "paused"}

    def server_resume(self):
        """
        Removes the flag file to signal the server to resume its operations.

        Returns:
            dict: A response indicating the server's resumed status or None if file not exists.
        """
        path = f"{os.getcwd()}\\server_side\\flag_file.txt"
        file = os.path.isfile(path)
        if file:
            os.remove(path)
            return {"server status": "resumed"}
        else:
            return None

    def server_uptime(self):
        """
        Calculates and returns the server's uptime by comparing the current time with the last recorded start time.

        Returns:
            str: The server uptime duration.
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        current_time = dt.datetime.now()
        server_start_time = self.db_utils.get_last_period_start_date(self.connection)
        server_uptime = current_time - dt.datetime.strptime(server_start_time, date_format)
        return str(server_uptime)

    def number_of_airplanes(self):
        """
        Retrieves the total number of airplanes being tracked for the current period.

        Returns:
            int: The number of airplanes.
        """
        all_airplanes = self.db_utils.get_all_airplanes_number_per_period(self.connection)
        return all_airplanes

    def airplanes_by_status(self, status):
        """
        Retrieves the number of airplanes with a specified status for the current period.

        Args:
            status (str): The status to filter the airplanes by.

        Returns:
            dict or list: A list of airplanes with the specified status.
        """
        airplanes_with_specified_status = self.db_utils.get_airplanes_with_specified_status_per_period(self.connection, status)
        return airplanes_with_specified_status

    def single_airplane_details(self, id):
        """
        Retrieves the details of a single airplane using its ID.

        Args:
            id (int): The ID of the airplane to retrieve details for.

        Returns:
            dict: The details of the specified airplane.
        """
        airplane_id = f"Airplane_{id}"
        airplane_details = self.db_utils.get_single_airplane_details(self.connection, airplane_id)
        return airplane_details


if __name__ == "__main__":
    api = API()
    serve(name = "127.0.0.1", port = 5000)
