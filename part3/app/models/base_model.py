import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """
    Abstract base model — Task 6.
    Maps id, created_at, updated_at to SQLAlchemy columns.
    All concrete models inherit from this class.
    """
    __abstract__ = True   # SQLAlchemy will NOT create a table for this class

    id         = db.Column(db.String(36), primary_key=True,
                           default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Flush updated_at and commit."""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data):
        """
        Update attributes from a dict.
        Protects id, created_at, updated_at from direct modification.
        """
        protected = {'id', 'created_at', 'updated_at'}
        for key, value in data.items():
            if key not in protected and hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        return {
            'id':         self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
