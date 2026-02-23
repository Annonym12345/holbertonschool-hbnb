#!/usr/bin/python3
"""Flask app"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Display n is a number"""
    return "{} is a number".format(n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def odd_or_even(n):
    """Display if number is odd or even"""
    return render_template("number_odd_or_even.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
