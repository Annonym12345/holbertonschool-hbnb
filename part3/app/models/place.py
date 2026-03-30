from app import db
from app.models.base_model import BaseModel
from app.models.amenity import place_amenity


class Place(BaseModel):
    """Place entity — Task 7 (mapping) + Task 8 (relationships)."""
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,        nullable=True, default='')
    price       = db.Column(db.Float,       nullable=False)
    latitude    = db.Column(db.Float,       nullable=False)
    longitude   = db.Column(db.Float,       nullable=False)
    owner_id    = db.Column(db.String(36),  db.ForeignKey('users.id'), nullable=False)

    # Relationships — Task 8
    owner     = db.relationship('User',    back_populates='places',  lazy=True)
    reviews   = db.relationship('Review',  back_populates='place',
                                 lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                 back_populates='places', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title       = title
        self.description = description
        self.price       = price
        self.latitude    = latitude
        self.longitude   = longitude
        self.owner_id    = owner_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters or less")
        self._title = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'title':       self.title,
            'description': self.description,
            'price':       self.price,
            'latitude':    self.latitude,
            'longitude':   self.longitude,
            'owner_id':    self.owner_id,
            'amenities':   [a.id for a in self.amenities]
        })
        return data
