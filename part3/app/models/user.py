import re
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    User entity — Task 1 (password hashing) + Task 6 (SQLAlchemy mapping).
    Password is ALWAYS hashed before storage and NEVER returned in responses.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50),  nullable=False)
    last_name  = db.Column(db.String(50),  nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean,     default=False, nullable=False)

    # Relationships — Task 8
    places  = db.relationship('Place',  back_populates='owner',
                               lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user',
                               lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.hash_password(password)   # Task 1
        self.is_admin   = is_admin

    # ------------------------------------------------------------------ #
    #  Validation helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_name(value, field):
        if not value or not isinstance(value, str):
            raise ValueError(f"{field} must be a non-empty string")
        if len(value) > 50:
            raise ValueError(f"{field} must be 50 characters or less")
        return value.strip()

    @staticmethod
    def _validate_email(value):
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value.lower().strip()

    # ------------------------------------------------------------------ #
    #  Property setters with validation
    # ------------------------------------------------------------------ #
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_name(value, 'First name')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_name(value, 'Last name')

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    # ------------------------------------------------------------------ #
    #  Password hashing — Task 1
    # ------------------------------------------------------------------ #
    def hash_password(self, plain_password):
        """Hash and store password using bcrypt."""
        if not plain_password or len(plain_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, plain_password):
        """Return True if plain_password matches stored hash."""
        return bcrypt.check_password_hash(self.password, plain_password)

    # ------------------------------------------------------------------ #
    #  Serialisation — password is NEVER included
    # ------------------------------------------------------------------ #
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin
            # password intentionally omitted
        })
        return data
