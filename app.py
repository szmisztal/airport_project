from flask import Flask


app = Flask(__name__)


@app.route("/start")
def start_airport():
    pass

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
