# Git Intro Project

# AirBnB Clone - HBNB v2 (Part 2)

## 📌 Description

This project is part of the AirBnB Clone series.  
In this part, we build a web application using **Flask**.  
We implement static and dynamic routes with different patterns, support variables and type converters, and use HTML templates.

---

## 🚀 Requirements

- Python 3
- Flask

Install Flask (locally or globally):

```bash
pip install flask
🗂️ Project Structure
part2/
├── 0-hello_route.py
├── 1-hbnb_route.py
├── 2-c_route.py
├── 3-number_route.py
├── 4-number_template.py
├── 5-number_odd_or_even.py
└── templates/
    ├── number.html
    └── number_odd_or_even.html
▶️ Running the Application

To start the web server, run any of the Python files:

python3 <filename>.py

For example:

python3 0-hello_route.py

The app will run by default on:

http://0.0.0.0:5000
🌐 Routes Implemented
Route	Description
/	Displays “Hello HBNB!”
/hbnb	Displays “HBNB”
/c/<text>	Displays “C <text>” with underscores replaced by spaces
/python/	Displays “Python is cool”
/python/<text>	Displays “Python <text>”
/number/<n>	Displays “<n> is a number” (only integers)
/number_template/<n>	Displays a page with “Number: <n>”
/number_odd_or_even/<n>	Displays an HTML page showing if <n> is odd or even
🧠 Concepts Used

Flask routing

Dynamic URLs

Type converters (int)

Templates with Jinja2

Conditional rendering in HTML

📄 Templates

Templates are stored in the templates/ directory and rendered with Flask:

number.html — Displays the number

number_odd_or_even.html — Displays number and whether it is odd or even

🧪 Testing the Routes

Use a browser or curl to test the endpoints:

Examples:

curl http://0.0.0.0:5000/
curl http://0.0.0.0:5000/hbnb
curl http://0.0.0.0:5000/c/hello_world
curl http://0.0.0.0:5000/python/
curl http://0.0.0.0:5000/python/rocks
curl http://0.0.0.0:5000/number/42
curl http://0.0.0.0:5000/number_template/42
curl http://0.0.0.0:5000/number_odd_or_even/42
