import os
import subprocess
import datetime as dt
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config, db_file
from server_side.connection_pool import Connection
from server_side.database_and_serialization_managment import DatabaseUtils



logger = logger_config("API logger", os.getcwd(), "api_logs.log")
app = Flask(__name__)
process = None


class APIMethods:
    def __init__(self):
        self.connection = Connection(db_file)
        self.db_utils = DatabaseUtils()

    def start(self):
        global process
        server_script_path = f"{os.getcwd()}/server_side/server.py"
        process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        logger.info(f"Started script with PID {process.pid}")
        return process

    def close(self):
        global process
        self.connection.connection.close()
        if process:
            process.terminate()
            process.wait()
            response = {"message": "Server stopped", "pid": process.pid}
            logger.info(f"Close script with PID {process.pid}")
            process = None
        else:
            response = {"error": "server is not running"}
            logger.info("Server is not running")
        return response

@app.route("/start")
def start_airport():
    process = api.start()
    return jsonify({"message": "Server started", "pid": process.pid})

@app.route("/close")
def close_airport():
    response = api.close()
    return jsonify(response)

@app.route("/pause")
def pause_airport():
    pass

@app.route("/restore")
def restore_airport():
    pass

@app.route("/uptime")
def uptime():
    date_format = "%Y-%m-%d %H:%M:%S"
    current_time = str(dt.datetime.now())
    server_start_time = db.get_last_period_start_date(conn)
    server_uptime = dt.datetime.strptime(current_time, date_format) - dt.datetime.strptime(server_start_time, date_format)
    return jsonify({"server uptime": server_uptime})

@app.route("/count_airplanes")
def count_airplanes():
    pass

@app.route("/collisions")
def collisions():
    pass

@app.route("/landings")
def successfully_landings():
    pass

@app.route("/airplanes_in_the_air")
def airplanes_in_the_air():
    pass

@app.route("/airplanes/<int:airplane_id>")
def airplane_detail(id):
    pass


if __name__ == "__main__":
    api = APIMethods()
    app.run(debug = True)
