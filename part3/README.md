HBnB - Part 3: Authentication, Authorization & Persistence
Description
Part 3 adds JWT authentication, role-based access control, and replaces the in-memory repository with a SQLAlchemy-backed SQLite database.
Installation
bashpip install -r requirements.txt
python run.py
API: http://127.0.0.1:5000/
Swagger: http://127.0.0.1:5000/api/v1/
Running Tests
bashpython -m unittest discover -s tests -v
Authors
Holberton School — HBnB Project Part 3
