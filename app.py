from flask import Flask
from client_side.client import Client
from server_side.server import Server
from server_side.connection_pool import ConnectionPool


app = Flask(__name__)

@app.route("/start_airport")
def start_airport():
    pass

@app.route("/pause_airport")
def pause_airport():
    pass

@app.route("/restore_airport")
def restore_airport():
    pass

@app.route("/close_airport")
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

@app.route("/successfully_landings")
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
