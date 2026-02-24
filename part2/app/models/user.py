"""User — entité utilisateur de l'application HBnB.

Attributs :
  - first_name : str, requis, max 50 chars
  - last_name  : str, requis, max 50 chars
  - email      : str, requis, format valide, unique (vérifié par la façade)
  - password   : str, requis (hashé en Part 3)
  - is_admin   : bool, False par défaut

Relations :
  - places  : liste des Place créés par cet utilisateur
  - reviews : liste des Review écrits par cet utilisateur
"""

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """Entité utilisateur."""

    def __init__(self, first_name: str, last_name: str,
                 email: str, password: str, is_admin: bool = False):
        super().__init__()

        # Validation
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name est requis et fait max 50 caractères")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name est requis et fait max 50 caractères")
        if not self._email_valide(email):
            raise ValueError(f"Format d'email invalide : {email}")
        if not password:
            raise ValueError("password est requis")

        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.password   = password   # sera hashé en Part 3
        self.is_admin   = is_admin

        # Relations (stockées en mémoire)
        self.places  = []
        self.reviews = []

    @staticmethod
    def _email_valide(email: str) -> bool:
        """Vérifie le format de l'email avec une regex simple."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return bool(re.match(pattern, email))

    def to_dict(self) -> dict:
        """Retourne le user en dict — sans le mot de passe."""
        return {
            'id':         self.id,
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
