from flask import Flask

app = Flask(__name__)

@app.route("/")
def airport_start():
    return "."

if __name__ == "__main__":
    app.run(debug=True)
