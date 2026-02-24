"""Amenity — équipement disponible dans un logement (WiFi, Piscine…).

Attributs :
  - name : str, requis, max 50 chars
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Entité équipement."""

    def __init__(self, name: str):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("name est requis et fait max 50 caractères")

        self.name = name

    def to_dict(self) -> dict:
        return {
            'id':         self.id,
            'name':       self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
