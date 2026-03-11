from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app import db

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    def get_by_email(self, email):
        return self.get_by_attribute('email', email)

class HBnBFacade:
    def __init__(self):
        self.user_repo    = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo   = SQLAlchemyRepository(Place)
        self.review_repo  = SQLAlchemyRepository(Review)

    # USERS
    def create_user(self, data):
        if self.user_repo.get_by_email(data.get('email', '')):
            raise ValueError("Email already registered")
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if not is_admin:
            data.pop('email', None)
            data.pop('password', None)
        new_email = data.get('email')
        if new_email and new_email != user.email:
            if self.user_repo.get_by_email(new_email):
                raise ValueError("Email already registered")
        if 'password' in data:
            user.hash_password(data.pop('password'))
        self.user_repo.update(user_id, data)
        return user

    # AMENITIES
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, data)
        return amenity

    # PLACES
    def create_place(self, data):
        if not self.user_repo.get(data.get('owner_id')):
            raise ValueError("Owner not found")
        amenity_ids = data.pop('amenities', [])
        place = Place(**data)
        for aid in amenity_ids:
            amenity = self.amenity_repo.get(aid)
            if amenity:
                place.amenities.append(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        amenity_ids = data.pop('amenities', None)
        if amenity_ids is not None:
            place.amenities = [
                self.amenity_repo.get(aid)
                for aid in amenity_ids
                if self.amenity_repo.get(aid)
            ]
            db.session.commit()
        self.place_repo.update(place_id, data)
        return place

    # REVIEWS
    def create_review(self, data, current_user_id=None):
        user_id  = data.get('user_id')
        place_id = data.get('place_id')
        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")
        existing = Review.query.filter_by(place_id=place_id, user_id=user_id).first()
        if existing:
            raise ValueError("You have already reviewed this place")
        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

facade = HBnBFacade()
