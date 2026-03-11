import re
from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50),  nullable=False)
    last_name  = db.Column(db.String(50),  nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)

    places  = db.relationship('Place',  backref='owner',  lazy=True,
                              cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True,
                              cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and max 50 chars")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and max 50 chars")
        if not self._valid_email(email):
            raise ValueError("Invalid email format")
        if not password:
            raise ValueError("password is required")
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.is_admin   = is_admin
        self.hash_password(password)

    @staticmethod
    def _valid_email(email):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))

    def hash_password(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, plain_password):
        return bcrypt.check_password_hash(self.password, plain_password)

    def to_dict(self):
        return {
            'id':         self.id,
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
