import os
import subprocess
import datetime as dt
from flask import Flask, jsonify
from common.config_variables import db_file, log_file
from common.logger_config import logger_config
from server_side.connection_pool import Connection
from server_side.database_managment import DatabaseUtils



app = Flask(__name__)


class API:
    """
    A class to control and interact with a server that processes and manages airplane data.

    Attributes:
        logger (Logger): Logger object to log information and errors.
        connection (Connection): Connection object to interact with the database.
        db_utils (DatabaseUtils): Utility object for database operations.
        process (subprocess.Popen): Represents the running server process.
    """

    def __init__(self):
        """
        Initializes the API class with default values and configurations.
        """
        self.logger = logger_config("Flask API logger", log_file, "flask_api_logs.log")
        self.connection = Connection(db_file)
        self.db_utils = DatabaseUtils()
        self.process = None

    def server_start(self):
        """
        Starts the server script as a subprocess and updates the API state.

        Returns:
            subprocess.Popen: The subprocess object for the running server.
        """
        server_script_path = f"{os.getcwd()}/server_side/server.py"
        self.process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
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


@app.route("/start", methods = ["GET"])
def start_airport():
    """
    Starts the airport server process.

    Returns:
        JSON response indicating that the server has started and its PID.
    """
    if api.process is None:
        process = api.server_start()
        return jsonify({"message": "Server started", "pid": process.pid}), 200
    else:
        return jsonify({"error": "server is running"}), 400

@app.route("/close", methods = ["GET"])
def close_airport():
    """
    Closes the airport server process.

    Returns:
        JSON response indicating that the server has stopped.
    """
    if api.process is not None:
        response = api.server_close()
        return jsonify(response), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/pause", methods = ["GET"])
def pause_airport():
    """
    Pauses the airport server operations.

    Returns:
        JSON response indicating that the server is paused.
    """
    if api.process is not None:
        response = api.server_pause()
        return jsonify(response), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/restore", methods = ["GET"])
def restore_airport():
    """
    Resumes the airport server operations.

    Returns:
        JSON response indicating that the server operations have been resumed.
    """
    if api.process is not None:
        resume_server = api.server_resume()
        if resume_server is None:
            return jsonify({"error": "server is working right now"}), 400
        else:
            return jsonify(resume_server), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/uptime", methods = ["GET"])
def uptime():
    """
    Provides the uptime of the airport server.

    Returns:
        JSON response with the server uptime duration.
    """
    if api.process is not None:
        server_uptime = api.server_uptime()
        return jsonify({"server uptime": server_uptime}), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/airplanes", methods = ["GET"])
def airplanes():
    """
    Retrieves the total number of airplanes.

    Returns:
        JSON response with the total number of airplanes.
    """
    if api.process is not None:
        airplanes = api.number_of_airplanes()
        return jsonify({"all airplanes number": airplanes}), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/collisions", methods = ["GET"])
def collisions():
    """
    Retrieves the list of airplanes that crashed due to running out of fuel and due to collision.

    Returns:
        JSON response with the list of airplanes crashed by running out of fuel and by collision.
    """
    if api.process is not None:
        airplanes_crashed_by_out_of_fuel = api.airplanes_by_status("CRASHED BY OUT OF FUEL")
        airplanes_crashed_by_collision = api.airplanes_by_status("CRASHED BY COLLISION")
        return jsonify({"airplanes crashed by out of fuel": airplanes_crashed_by_out_of_fuel,
                        "airplanes crashed by collision": airplanes_crashed_by_collision}), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/landings", methods = ["GET"])
def successful_landings():
    """
    Retrieves the list of airplanes that landed successfully.

    Returns:
        JSON response with the list of airplanes that had a successful landing.
    """
    if api.process is not None:
        airplanes_with_successfully_landings = api.airplanes_by_status("SUCCESSFULLY LANDING")
        return jsonify({"airplanes with successfully landing": airplanes_with_successfully_landings}), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/in_the_air", methods = ["GET"])
def airplanes_in_the_air():
    """
    Retrieves the list of airplanes that are currently in the air.

    Returns:
        JSON response with the list of airplanes that are in the air.
    """
    if api.process is not None:
        planes_in_the_air = api.airplanes_by_status(None)
        return jsonify({"airplanes in the air": planes_in_the_air}), 200
    else:
        return jsonify({"error": "server is not running"}), 400

@app.route("/airplanes/<int:airplane_id>", methods = ["GET"])
def airplane_detail(airplane_id):
    """
    Retrieves details of a specific airplane by its ID.

    Args:
        airplane_id (int): The ID of the airplane.

    Returns:
        JSON response with the details of the specified airplane or an error message if the airplane ID does not exist.
    """
    if api.process is not None:
        airplane = api.single_airplane_details(airplane_id)
        if airplane == None:
            return jsonify({"error": "there is no airplane with this id"}), 404
        id = airplane[0]
        airplane_appearance_date = airplane[1]
        status = airplane[2]
        if status == None:
            status = "In the air"
        return jsonify({"airplane details":
                            {"id": id,
                             "appearance_date": airplane_appearance_date,
                             "status": status}}), 200
    else:
        return jsonify({"error": "server is not running"}), 400


if __name__ == "__main__":
    api = API()
    app.run(debug = True)
