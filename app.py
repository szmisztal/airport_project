import os
import subprocess
import datetime as dt
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config, db_file
from server_side.connection_pool import Connection
from server_side.database_and_serialization_managment import DatabaseUtils



app = Flask(__name__)


class API:
    """
    A class to control and interact with a server that processes and manages airplane data.

    Attributes:
        is_running (bool): Flag indicating whether the server is running.
        logger (Logger): Logger object to log information and errors.
        connection (Connection): Connection object to interact with the database.
        db_utils (DatabaseUtils): Utility object for database operations.
        process (subprocess.Popen): Represents the running server process.
        response_when_server_is_not_running (dict): Default response when the server is not running.
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
        self.response_when_server_is_not_running = {"error": "server is not running"}

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
            dict: A response message indicating the server has stopped or an error message if the server wasn't running.
        """
        if self.is_running:
            self.process.terminate()
            self.process.wait()
            response = {"message": "Server stopped", "pid": self.process.pid}
            self.logger.info(f"Close script with PID {self.process.pid}")
            self.process = None
            self.db_utils.update_period_end(self.connection)
            self.connection.connection.close()
            return response
        else:
            return self.response_when_server_is_not_running

    def server_pause(self):
        """
        Creates a flag file to signal the server to pause its operations.

        Returns:
            dict: A response indicating the server's paused status or an error message if the server wasn't running.
        """
        if self.is_running:
            path = f"{os.getcwd()}\\server_side\\flag_file.txt"
            with open(path, "w"):
                pass
            response = {"server status": "paused"}
            return response
        else:
            return self.response_when_server_is_not_running

    def server_resume(self):
        """
        Removes the flag file to signal the server to resume its operations.

        Returns:
            dict: A response indicating the server's resumed status or an error message if the server wasn't running or wasn't paused.
        """
        if self.is_running:
            path = f"{os.getcwd()}\\server_side\\flag_file.txt"
            file = os.path.isfile(path)
            if file:
                os.remove(path)
                response = {"server status": "resumed"}
                return response
            else:
                return self.response_when_server_is_not_running
        else:
            return self.response_when_server_is_not_running

    def server_uptime(self):
        """
        Calculates and returns the server's uptime by comparing the current time with the last recorded start time.

        Returns:
            str: The server uptime duration or an error message if the server isn't running.
        """
        if self.is_running:
            date_format = "%Y-%m-%d %H:%M:%S"
            current_time = dt.datetime.now()
            server_start_time = self.db_utils.get_last_period_start_date(self.connection)
            server_uptime = current_time - dt.datetime.strptime(server_start_time, date_format)
            return str(server_uptime)
        else:
            return self.response_when_server_is_not_running

    def number_of_airplanes(self):
        """
        Retrieves the total number of airplanes being tracked for the current period.

        Returns:
            dict or int: The number of airplanes or an error message if the server isn't running.
        """
        if self.is_running:
            all_airplanes = self.db_utils.get_all_airplanes_number_per_period(self.connection)
            return all_airplanes
        else:
            return self.response_when_server_is_not_running

    def airplanes_by_status(self, status):
        """
        Retrieves the number of airplanes with a specified status for the current period.

        Args:
            status (str): The status to filter the airplanes by.

        Returns:
            dict or list: A list of airplanes with the specified status or an error message if the server isn't running.
        """
        if self.is_running:
            airplanes_with_specified_status = self.db_utils.get_airplanes_with_specified_status_per_period(self.connection, status)
            return airplanes_with_specified_status
        else:
            return self.response_when_server_is_not_running

    def single_airplane_details(self, id):
        """
        Retrieves the details of a single airplane using its ID.

        Args:
            id (int): The ID of the airplane to retrieve details for.

        Returns:
            dict: The details of the specified airplane or an error message if the server isn't running.
        """
        if self.is_running:
            airplane_id = f"Airplane_{id}"
            airplane_details = self.db_utils.get_single_airplane_details(self.connection, airplane_id)
            return airplane_details
        else:
            return self.response_when_server_is_not_running


@app.route("/start")
def start_airport():
    """
    Starts the airport server process.

    Returns:
        JSON response indicating that the server has started and its PID.
    """
    process = api.server_start()
    return jsonify({"message": "Server started", "pid": process.pid})

@app.route("/close")
def close_airport():
    """
    Closes the airport server process.

    Returns:
        JSON response indicating that the server has stopped.
    """
    response = api.server_close()
    return jsonify(response)

@app.route("/pause")
def pause_airport():
    """
    Pauses the airport server operations.

    Returns:
        JSON response indicating that the server is paused.
    """
    pause_server = api.server_pause()
    return jsonify(pause_server)

@app.route("/restore")
def restore_airport():
    """
    Resumes the airport server operations.

    Returns:
        JSON response indicating that the server operations have been resumed.
    """
    resume_server = api.server_resume()
    return jsonify(resume_server)

@app.route("/uptime")
def uptime():
    """
    Provides the uptime of the airport server.

    Returns:
        JSON response with the server uptime duration.
    """
    server_uptime = api.server_uptime()
    return jsonify({"server uptime": server_uptime})

@app.route("/airplanes")
def airplanes():
    """
    Retrieves the total number of airplanes.

    Returns:
        JSON response with the total number of airplanes.
    """
    airplanes = api.number_of_airplanes()
    return jsonify({"all airplanes number": airplanes})

@app.route("/collisions")
def collisions():
    """
    Retrieves the list of airplanes that crashed due to running out of fuel and due to collision.

    Returns:
        JSON response with the list of airplanes crashed by running out of fuel and by collision.
    """
    airplanes_crashed_by_out_of_fuel = api.airplanes_by_status("CRASHED BY OUT OF FUEL")
    airplanes_crashed_by_collision = api.airplanes_by_status("CRASHED BY COLLISION")
    return jsonify({"airplanes crashed by out of fuel": airplanes_crashed_by_out_of_fuel,
                    "airplanes crashed by collision": airplanes_crashed_by_collision})

@app.route("/landings")
def successfully_landings():
    """
    Retrieves the list of airplanes that landed successfully.

    Returns:
        JSON response with the list of airplanes that had a successful landing.
    """
    airplanes_with_successfully_landings = api.airplanes_by_status("SUCCESSFULLY LANDING")
    return jsonify({"airplanes with successfully landing": airplanes_with_successfully_landings})

@app.route("/airplanes_in_the_air")
def airplanes_in_the_air():
    """
    Retrieves the list of airplanes that are currently in the air.

    Returns:
        JSON response with the list of airplanes that are in the air.
    """
    planes_in_the_air = api.airplanes_by_status(None)
    return jsonify({"airplanes in the air": planes_in_the_air})

@app.route("/airplanes/<int:airplane_id>")
def airplane_detail(airplane_id):
    """
    Retrieves details of a specific airplane by its ID.

    Args:
        airplane_id (int): The ID of the airplane.

    Returns:
        JSON response with the details of the specified airplane or an error message if the airplane ID does not exist.
    """
    airplane = api.single_airplane_details(airplane_id)
    if airplane == None:
        return jsonify({"error": "there is no airplane with this id"})
    id = airplane[0]
    airplane_appearance_date = airplane[1]
    status = airplane[2]
    if status == None:
        status = "In the air"
    return jsonify({"airplane details":
                        {"id": id,
                         "appearance_date": airplane_appearance_date,
                         "status": status}
                    })


if __name__ == "__main__":
    api = API()
    app.run(debug = True)
