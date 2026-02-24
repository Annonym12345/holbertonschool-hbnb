"""Review — avis laissé par un utilisateur sur un logement.

Attributs :
  - text     : str, requis
  - rating   : int, entre 1 et 5
  - place_id : str, UUID du Place concerné
  - user_id  : str, UUID du User auteur
"""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """Entité avis/commentaire."""

    def __init__(self, text: str, rating: int, place_id: str, user_id: str):
        super().__init__()

        if not text:
            raise ValueError("text est requis")
        if not (1 <= int(rating) <= 5):
            raise ValueError("rating doit être entre 1 et 5")
        if not place_id:
            raise ValueError("place_id est requis")
        if not user_id:
            raise ValueError("user_id est requis")

        self.text     = text
        self.rating   = int(rating)
        self.place_id = place_id
        self.user_id  = user_id

    def to_dict(self) -> dict:
        return {
            'id':         self.id,
            'text':       self.text,
            'rating':     self.rating,
            'place_id':   self.place_id,
            'user_id':    self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
