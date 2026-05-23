import os
from flask import Flask, send_from_directory

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
