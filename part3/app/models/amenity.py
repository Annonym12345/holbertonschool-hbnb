from app import db
from app.models.base_model import BaseModel

# Association table for Place <-> Amenity (many-to-many) — Task 8
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id',   db.String(36), db.ForeignKey('places.id'),   primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    """Amenity entity — Task 7 (mapping) + Task 8 (relationships)."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    # Relationship — Task 8
    places = db.relationship('Place', secondary=place_amenity,
                              back_populates='amenities', lazy=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or less")
        self._name = value.strip()

    def to_dict(self):
        data = super().to_dict()
        data.update({'name': self.name})
        return data
