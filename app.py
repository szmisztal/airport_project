from flask import Flask
from client import Client

app = Flask(__name__)

@app.route("/")
def airport_start():
    c = Client()
    c.start()
    return "."

if __name__ == "__main__":
    app.run(debug = True)
