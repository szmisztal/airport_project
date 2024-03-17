import os
import subprocess
import datetime as dt
from jsonrpcserver import serve, method, Success
from config_variables_for_server_and_client import logger_config, db_file
from server_side.database_and_serialization_managment import DatabaseUtils
from server_side.connection_pool import Connection


logger = logger_config("RPC API logger", os.getcwd(), "rpc_api_logs.log")
db_utils = DatabaseUtils()
connection = Connection(db_file)
process = None

@method
def server_start():
    server_script_path = f"{os.getcwd()}/server_side/server.py"
    process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    logger.info(f"Started script with PID {process.pid}")
    return Success({"message": f"Server started with PID: {process.pid}"})

@method
def server_close():
    process.terminate()
    process.wait()
    logger.info(f"Close script with PID {process.pid}")
    db_utils.update_period_end(connection)
    connection.connection.close()
    return {"message": f"Server with {process.pid} stopped"}

@method
def server_pause():
    path = f"{os.getcwd()}\\server_side\\flag_file.txt"
    with open(path, "w"):
        pass
    return {"server status": "paused"}

@method
def server_resume():
    path = f"{os.getcwd()}\\server_side\\flag_file.txt"
    file = os.path.isfile(path)
    if file:
        os.remove(path)
        return {"server status": "resumed"}
    else:
        return None

@method
def server_uptime():
    date_format = "%Y-%m-%d %H:%M:%S"
    current_time = dt.datetime.now()
    server_start_time = db_utils.get_last_period_start_date(connection)
    server_uptime = current_time - dt.datetime.strptime(server_start_time, date_format)
    return str(server_uptime)

@method
def number_of_airplanes():
    all_airplanes = db_utils.get_all_airplanes_number_per_period(connection)
    return all_airplanes

@method
def airplanes_by_status(status):
    airplanes_with_specified_status = db_utils.get_airplanes_with_specified_status_per_period(connection, status)
    return airplanes_with_specified_status

@method
def single_airplane_details(id):
    airplane_id = f"Airplane_{id}"
    airplane_details = db_utils.get_single_airplane_details(connection, airplane_id)
    return airplane_details


if __name__ == "__main__":
    serve(name = "127.0.0.1", port = 5000)
