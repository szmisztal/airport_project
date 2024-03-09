import os
import subprocess
import datetime as dt
from flask import Flask, jsonify
from config_variables_for_server_and_client import logger_config, db_file
from server_side.connection_pool import Connection
from server_side.database_and_serialization_managment import DatabaseUtils



app = Flask(__name__)


class API:
    def __init__(self):
        self.is_running = False
        self.logger = logger_config("API logger", os.getcwd(), "api_logs.log")
        self.connection = Connection(db_file)
        self.db_utils = DatabaseUtils()
        self.process = None
        self.response_when_server_is_not_running = {"error": "server is not running"}

    def server_start(self):
        server_script_path = f"{os.getcwd()}/server_side/server.py"
        self.process = subprocess.Popen(["python", server_script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        self.is_running = True
        self.logger.info(f"Started script with PID {self.process.pid}")
        return self.process

    def server_close(self):
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
        pass

    def server_resume(self):
        pass

    def server_uptime(self):
        if self.is_running:
            date_format = "%Y-%m-%d %H:%M:%S"
            current_time = dt.datetime.now()
            server_start_time = self.db_utils.get_last_period_start_date(self.connection)
            server_uptime = current_time - dt.datetime.strptime(server_start_time, date_format)
            return str(server_uptime)
        else:
            return self.response_when_server_is_not_running

    def number_of_airplanes(self):
        if self.is_running:
            all_airplanes = self.db_utils.get_all_airplanes_number_per_period(self.connection)
            return all_airplanes
        else:
            return self.response_when_server_is_not_running

    def airplanes_by_status(self, status):
        if self.is_running:
            airplanes_with_specified_status = self.db_utils.get_airplanes_with_specified_status_per_period(self.connection, status)
            return airplanes_with_specified_status
        else:
            return self.response_when_server_is_not_running

    def single_airplane_details(self, id):
        if self.is_running:
            airplane_id = f"Airplane_{id}"
            airplane_details = self.db_utils.get_single_airplane_details(self.connection, airplane_id)
            return airplane_details
        else:
            return self.response_when_server_is_not_running


@app.route("/start")
def start_airport():
    process = api.server_start()
    return jsonify({"message": "Server started", "pid": process.pid})

@app.route("/close")
def close_airport():
    response = api.server_close()
    return jsonify(response)

@app.route("/pause")
def pause_airport():
    pass

@app.route("/restore")
def restore_airport():
    pass

@app.route("/uptime")
def uptime():
    server_uptime = api.server_uptime()
    return jsonify({"server uptime": server_uptime})

@app.route("/airplanes")
def airplanes():
    airplanes = api.number_of_airplanes()
    return jsonify({"all airplanes number": airplanes})

@app.route("/collisions")
def collisions():
    airplanes_crashed_by_out_of_fuel = api.airplanes_by_status("CRASHED BY OUT OF FUEL")
    airplanes_crashed_by_collision = api.airplanes_by_status("CRASHED BY COLLISION")
    return jsonify({"airplanes crashed by out of fuel": airplanes_crashed_by_out_of_fuel,
                    "airplanes crashed by collision": airplanes_crashed_by_collision})

@app.route("/landings")
def successfully_landings():
    airplanes_with_successfully_landings = api.airplanes_by_status("SUCCESSFULLY LANDING")
    return jsonify({"airplanes with successfully landing": airplanes_with_successfully_landings})

@app.route("/airplanes_in_the_air")
def airplanes_in_the_air():
    planes_in_the_air = api.airplanes_by_status(None)
    return jsonify({"airplanes in the air": planes_in_the_air})

@app.route("/airplanes/<int:airplane_id>")
def airplane_detail(airplane_id):
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
