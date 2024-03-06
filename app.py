import os
import subprocess
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config


logger = logger_config("API logger", os.getcwd(), "api_logs.log")
app = Flask(__name__)
process = None


@app.route("/start")
def start_airport():
    global process
    server_script_path = f"{os.getcwd()}/server_side/server.py"
    process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    logger.info(f"Started script with PID {process.pid}")
    return jsonify({"message": "Server started", "pid": process.pid})

@app.route("/close")
def close_airport():
    global process
    if process:
        process.terminate()
        process.wait()
        response = {"message": "Server stopped", "pid": process.pid}
        logger.info(f"Close script with PID {process.pid}")
        process = None
        return jsonify(response)
    else:
        response = {"error": "server is not running"}
        logger.info("Server is not running")
    return jsonify(response)

@app.route("/pause")
def pause_airport():
    pass

@app.route("/restore")
def restore_airport():
    pass

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
