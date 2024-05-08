import os
import subprocess
import datetime as dt
from jsonrpcserver import serve, method, Success, Error
from common.config_variables import db_file
from common.logger_config import logger_config
from server_side.database_managment import DatabaseUtils
from server_side.connection_pool import Connection


logger = logger_config("RPC API logger", os.getcwd(), "rpc_api_logs.log")
db_utils = DatabaseUtils()
connection = Connection(db_file)
process = None

def establish_server_script_file_dir():
    """
    Establishes the directory path for the server script file.

    Returns:
        str: The absolute path to the server script directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    server_script_path = os.path.join(parent_dir, "server_side")
    return server_script_path


@method
def server_start():
    """
    Starts the server process if it is not already running.

    Returns:
        Success: A success message including the PID of the started process.
        Error: An error message if the server is already running.
    """
    global process
    if process is None:
        server_script_dir = establish_server_script_file_dir()
        process = subprocess.Popen(["python", f"{server_script_dir}\server.py"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        logger.info(f"Started script with PID {process.pid}")
        return Success({"message": f"Server started with PID: {process.pid}"})
    else:
        return Error(code = -32000, message = "Server is running right now")

@method
def server_close():
    """
    Terminates the server process if it is running, updates the database, and closes the connection.

    Returns:
        Success: A success message including the PID of the stopped process.
        Error: An error message if the server is not running.
    """
    if process is not None:
        process.terminate()
        process.wait()
        logger.info(f"Close script with PID {process.pid}")
        db_utils.update_period_end(connection)
        connection.connection.close()
        return Success({"message": f"Server with {process.pid} stopped"})
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def server_pause():
    """
    Pauses the server process by creating a flag file, indicating that the server is paused.

    Returns:
        Success: A success message indicating that the server is paused.
        Error: An error message if the server is not running.
    """
    if process is not None:
        path = establish_server_script_file_dir()
        with open(f"{path}\\flag_file.txt", "w"):
            pass
        return Success({"server status": "paused"})
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def server_resume():
    """
    Resumes the server process by removing the flag file if it exists, indicating that the server is resumed.

    Returns:
        Success: A success message indicating that the server is resumed.
        Error: An error message if the flag file does not exist or the server is not running.
    """
    if process is not None:
        server_script_dir = establish_server_script_file_dir()
        path = f"{server_script_dir}\\flag_file.txt"
        file = os.path.isfile(path)
        if file:
            os.remove(path)
            return Success({"server status": "resumed"})
        else:
            return Error(code = -32001, message = "Temp file not found")
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def server_uptime():
    """
    Calculates and returns the uptime of the server.

    Returns:
        Success: A success message with the server's uptime.
        Error: An error message if the server is not running.
    """
    if process is not None:
        date_format = "%Y-%m-%d %H:%M:%S"
        current_time = dt.datetime.now()
        server_start_time = db_utils.get_last_period_start_date(connection)
        server_uptime = current_time - dt.datetime.strptime(server_start_time, date_format)
        return Success({"server uptime": str(server_uptime)})
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def number_of_airplanes():
    """
    Retrieves the number of airplanes processed during the current period.

    Returns:
        Success: A success message with the number of airplanes.
        Error: An error message if the server is not running.
    """
    if process is not None:
        all_airplanes = db_utils.get_all_airplanes_number_per_period(connection)
        return Success({"airplanes number": all_airplanes})
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def airplanes_by_status(status):
    """
    Retrieves the number of airplanes with a specified status.

    Args:
        status (str): The status to filter the airplanes by.

    Returns:
        Success: A success message with the list of airplanes with the specified status.
        Error: An error message if the server is not running.
    """
    if process is not None:
        airplanes_with_specified_status = db_utils.get_airplanes_with_specified_status_per_period(connection, status)
        return Success({f"airplanes {status}": airplanes_with_specified_status})
    else:
        return Error(code = -32000, message = "Server is not running")

@method
def single_airplane_details(id):
    """
    Retrieves details for a single airplane based on its ID.

    Args:
        id (int): The ID of the airplane.

    Returns:
        Success: A success message with the airplane details.
        Error: An error message if the airplane with the specified ID is not found or the server is not running.
    """
    if process is not None:
        airplane_id = f"Airplane_{id}"
        airplane_details = db_utils.get_single_airplane_details(connection, airplane_id)
        if airplane_details == None:
            return Error(code = -32002, message = f"Airplane with {id} ID not found")
        return Success({airplane_id: airplane_details})
    else:
        return Error(code = -32000, message = "Server is not running")


if __name__ == "__main__":
    serve(name = "127.0.0.1", port = 5000)


