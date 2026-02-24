"""Place — logement proposé à la location.

Attributs :
  - title       : str, requis, max 100 chars
  - description : str, optionnel
  - price       : float, >= 0
  - latitude    : float, entre -90.0 et 90.0
  - longitude   : float, entre -180.0 et 180.0
  - owner_id    : str, UUID du User propriétaire

Relations :
  - amenities : liste d'objets Amenity
  - reviews   : liste d'objets Review
"""

from app.models.base_model import BaseModel


class Place(BaseModel):
    """Entité logement."""

    def __init__(self, title: str, description: str,
                 price: float, latitude: float, longitude: float,
                 owner_id: str):
        super().__init__()

        # Validation des attributs
        if not title or len(title) > 100:
            raise ValueError("title est requis et fait max 100 caractères")
        if float(price) < 0:
            raise ValueError("price doit être >= 0")
        if not (-90.0 <= float(latitude) <= 90.0):
            raise ValueError("latitude doit être entre -90.0 et 90.0")
        if not (-180.0 <= float(longitude) <= 180.0):
            raise ValueError("longitude doit être entre -180.0 et 180.0")
        if not owner_id:
            raise ValueError("owner_id est requis")

        self.title       = title
        self.description = description or ''
        self.price       = float(price)
        self.latitude    = float(latitude)
        self.longitude   = float(longitude)
        self.owner_id    = owner_id

        # Relations (stockées en mémoire)
        self.amenities = []
        self.reviews   = []

    def to_dict(self) -> dict:
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
