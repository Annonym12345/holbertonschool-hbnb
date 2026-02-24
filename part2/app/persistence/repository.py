"""Repository pattern — abstraction de la couche de stockage.

Repository (ABC)
    └── InMemoryRepository   ← utilisé en Part 2
         └── (SQLAlchemy)    ← sera implémenté en Part 3

L'interface est identique : on pourra swapper sans toucher à la façade.
"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Interface abstraite que tout repository doit respecter."""

    @abstractmethod
    def add(self, obj):
        """Ajoute un objet au stockage."""
        pass

    @abstractmethod
    def get(self, obj_id: str):
        """Retourne l'objet correspondant à l'id, ou None."""
        pass

    @abstractmethod
    def get_all(self) -> list:
        """Retourne tous les objets stockés."""
        pass

    @abstractmethod
    def update(self, obj_id: str, data: dict):
        """Met à jour un objet existant avec les données du dict."""
        pass

    @abstractmethod
    def delete(self, obj_id: str):
        """Supprime un objet par son id."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value):
        """Retourne le premier objet dont l'attribut correspond à la valeur."""
        pass


class InMemoryRepository(Repository):
    """Stockage en mémoire vive (dict Python).

    Clé   = obj.id (str UUID4)
    Valeur = instance de l'objet
    """

    def __init__(self):
        self._storage: dict = {}

    def add(self, obj):
        """Enregistre l'objet avec son id comme clé."""
        self._storage[obj.id] = obj

    def get(self, obj_id: str):
        """Récupère un objet par son id (None si absent)."""
        return self._storage.get(obj_id)

    def get_all(self) -> list:
        """Retourne tous les objets sous forme de liste."""
        return list(self._storage.values())

    def update(self, obj_id: str, data: dict):
        """Applique les nouvelles valeurs sur l'objet existant."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id: str):
        """Supprime l'objet du stockage."""
        self._storage.pop(obj_id, None)

    def get_by_attribute(self, attr_name: str, attr_value):
        """Recherche linéaire sur l'attribut donné (O(n))."""
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None
        )
