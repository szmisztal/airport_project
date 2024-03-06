import os
import subprocess
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config


app = Flask(__name__)
logger = logger_config("API logger", os.getcwd(), "api_logs.log")


@app.route("/start")
def start_airport():
    server_script_path = f"{os.getcwd()}/server_side/server.py"
    process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    stdout, stderr = process.communicate()
    logger.info(f"{process.returncode} - stdout: {stdout}, stderr: {stderr}")
    return jsonify({
        "stdout": stdout,
        "stderr": stderr,
        "returncode": process.returncode
    })

@app.route("/pause")
def pause_airport():
    pass

@app.route("/restore")
def restore_airport():
    pass

@app.route("/close")
def close_airport():
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
