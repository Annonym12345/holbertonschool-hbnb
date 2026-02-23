#!/usr/bin/python3
"""Flask app"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Display number in HTML"""
    return render_template("number.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
