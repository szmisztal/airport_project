from flask import Flask
from client_side.client import Client
from server_side.server import Server
from server_side.connection_pool import ConnectionPool


app = Flask(__name__)

@app.route("/")
def airport_start():
    c = ConnectionPool(10, 100)
    s = Server(c)
    s.start()
    return "."

if __name__ == "__main__":
    app.run(debug = True)
