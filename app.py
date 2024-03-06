import os
import subprocess
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config


app = Flask(__name__)
logger = logger_config("API logger", os.getcwd(), "api_logs.log")
process = None
server_process_pid = {}


@app.route("/start")
def start_airport():
    global process
    server_script_path = f"{os.getcwd()}/server_side/server.py"
    process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    logger.info(f"Started script with PID {process.pid}")
    server_process_pid["server_process_pid"] = process.pid
    return jsonify({"message": "Server started", "pid": process.pid})

@app.route("/pause")
def pause_airport():
    pass

@app.route("/restore")
def restore_airport():
    pass

@app.route("/close")
def close_airport():
    global process
    process_pid = server_process_pid.get("server_process_pid")
    if process:
        process.terminate()
        process.wait()
        logger.info(f"Close script with PID {process_pid}")
        return jsonify({"message": "Server`s close", "pid": process_pid})
    else:
        logger.info("Server is not running")
        return jsonify({"error": "server is not running"})

@app.route("/uptime")
def uptime():
    pass

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
    app.run(debug = True)
