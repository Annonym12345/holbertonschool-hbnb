from app import db
from app.models.base_model import BaseModel

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id',   db.String(36), db.ForeignKey('places.id'),    primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("name is required and max 50 chars")
        self.name = name

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
