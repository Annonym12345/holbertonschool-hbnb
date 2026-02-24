"""HBnBFacade — point d'entrée unique pour toute la logique métier.

Pattern Facade :
  Les namespaces API n'appellent QUE cette façade.
  La façade appelle les repositories et les modèles.
  Ainsi, l'API ne connaît pas le stockage, et le stockage ne connaît pas l'API.

                API (namespaces)
                      │
                  HBnBFacade
                 /    |    \   \
          UserRepo  PlaceRepo  AmenityRepo  ReviewRepo
"""

from app.models.user     import User
from app.models.amenity  import Amenity
from app.models.place    import Place
from app.models.review   import Review
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Orchestre toutes les opérations CRUD entre l'API et les repositories."""

    def __init__(self):
        self.user_repo    = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo   = InMemoryRepository()
        self.review_repo  = InMemoryRepository()

    # ================================================================ USERS

    def create_user(self, data: dict) -> User:
        """Crée un utilisateur — vérifie l'unicité de l'email."""
        if self.user_repo.get_by_attribute('email', data.get('email')):
            raise ValueError("Cet email est déjà utilisé")
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> list:
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict) -> User | None:
        """Met à jour un user — vérifie l'unicité si l'email change."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        new_email = data.get('email')
        if new_email and new_email != user.email:
            if self.user_repo.get_by_attribute('email', new_email):
                raise ValueError("Cet email est déjà utilisé")
        self.user_repo.update(user_id, data)
        return user

    # =========================================================== AMENITIES

    def create_amenity(self, data: dict) -> Amenity:
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Amenity | None:
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> list:
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, data: dict) -> Amenity | None:
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, data)
        return amenity

    # ============================================================== PLACES

    def create_place(self, data: dict) -> Place:
        """Crée un logement — vérifie que le owner existe."""
        owner_id = data.get('owner_id')
        if not self.user_repo.get(owner_id):
            raise ValueError(f"Owner introuvable : id='{owner_id}'")

        # Extrait les ids d'amenities avant de passer au constructeur Place
        amenity_ids = data.pop('amenities', [])
        place = Place(**data)

        # Résolution des amenities
        for aid in amenity_ids:
            amenity = self.amenity_repo.get(aid)
            if amenity:
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Place | None:
        return self.place_repo.get(place_id)

    def get_all_places(self) -> list:
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict) -> Place | None:
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Mise à jour de la liste d'amenities si fournie
        amenity_ids = data.pop('amenities', None)
        if amenity_ids is not None:
            place.amenities = [
                self.amenity_repo.get(aid)
                for aid in amenity_ids
                if self.amenity_repo.get(aid)
            ]
        self.place_repo.update(place_id, data)
        return place

    # ============================================================= REVIEWS

    def create_review(self, data: dict) -> Review:
        """Crée un avis — vérifie que user et place existent."""
        if not self.user_repo.get(data.get('user_id')):
            raise ValueError("Utilisateur introuvable")
        if not self.place_repo.get(data.get('place_id')):
            raise ValueError("Logement introuvable")

        review = Review(**data)
        self.review_repo.add(review)

        # Lien vers le place
        place = self.place_repo.get(review.place_id)
        if place:
            place.reviews.append(review)

        return review

    def get_review(self, review_id: str) -> Review | None:
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> list:
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str) -> list:
        return [r for r in self.review_repo.get_all()
                if r.place_id == place_id]

    def update_review(self, review_id: str, data: dict) -> Review | None:
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, data)
        return review

    def delete_review(self, review_id: str) -> bool:
        """Supprime un avis et le retire de la liste du place associé."""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        place = self.place_repo.get(review.place_id)
        if place and review in place.reviews:
            place.reviews.remove(review)
        self.review_repo.delete(review_id)
        return True


# Instance singleton partagée dans toute l'application
facade = HBnBFacade()
