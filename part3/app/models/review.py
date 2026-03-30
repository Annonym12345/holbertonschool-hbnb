from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review entity — Task 7 (mapping) + Task 8 (relationships)."""
    __tablename__ = 'reviews'

    text     = db.Column(db.Text,       nullable=False)
    rating   = db.Column(db.Integer,    nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'),  nullable=False)

    # Relationships — Task 8
    place = db.relationship('Place', back_populates='reviews', lazy=True)
    user  = db.relationship('User',  back_populates='reviews', lazy=True)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text     = text
        self.rating   = rating
        self.place_id = place_id
        self.user_id  = user_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Text must be a non-empty string")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'text':     self.text,
            'rating':   self.rating,
            'place_id': self.place_id,
            'user_id':  self.user_id
        })
        return data
