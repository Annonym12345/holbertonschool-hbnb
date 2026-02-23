#!/usr/bin/python3
"""Flask app"""
from flask import Flask

app = Flask(__name__)


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Display C followed by text"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    """Display Python followed by text"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
