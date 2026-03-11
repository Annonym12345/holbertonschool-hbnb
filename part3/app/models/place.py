from app import db
from app.models.base_model import BaseModel
from app.models.amenity import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,        nullable=True,  default='')
    price       = db.Column(db.Float,       nullable=False)
    latitude    = db.Column(db.Float,       nullable=False)
    longitude   = db.Column(db.Float,       nullable=False)
    owner_id    = db.Column(db.String(36),  db.ForeignKey('users.id'), nullable=False)

    amenities = db.relationship('Amenity', secondary=place_amenity,
                                backref=db.backref('places', lazy=True), lazy=True)
    reviews   = db.relationship('Review', backref='place', lazy=True,
                                cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("title is required and max 100 chars")
        if float(price) < 0:
            raise ValueError("price must be a non-negative value")
        if not (-90.0 <= float(latitude) <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        if not (-180.0 <= float(longitude) <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        if not owner_id:
            raise ValueError("owner_id is required")
        self.title       = title
        self.description = description or ''
        self.price       = float(price)
        self.latitude    = float(latitude)
        self.longitude   = float(longitude)
        self.owner_id    = owner_id

    def update(self, data):
        if 'price' in data and float(data['price']) < 0:
            raise ValueError("price must be a non-negative value")
        if 'latitude' in data and not (-90.0 <= float(data['latitude']) <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        if 'longitude' in data and not (-180.0 <= float(data['longitude']) <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        for f in ('price', 'latitude', 'longitude'):
            if f in data:
                data[f] = float(data[f])
        super().update(data)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description,
            'price':       self.price,
            'latitude':    self.latitude,
            'longitude':   self.longitude,
            'owner_id':    self.owner_id,
            'created_at':  self.created_at.isoformat(),
            'updated_at':  self.updated_at.isoformat(),
        }
