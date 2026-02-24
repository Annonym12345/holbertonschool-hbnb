"""BaseModel — classe mère de toutes les entités HBnB.

Fournit :
  - id         : UUID4 unique généré automatiquement
  - created_at : datetime de création (UTC)
  - updated_at : datetime de dernière modification (UTC)
  - save()     : met à jour updated_at
  - update()   : applique un dict de modifications
"""

import uuid
from datetime import datetime, timezone


class BaseModel:
    """Classe de base héritée par User, Place, Review, Amenity."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def save(self):
        """Met à jour le timestamp de modification."""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data: dict):
        """Applique les valeurs du dict sur les attributs existants."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
