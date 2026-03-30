from app.persistence.repository import SQLAlchemyRepository
from app.models.user    import User
from app.models.amenity import Amenity
from app.models.place   import Place
from app.models.review  import Review
from app import db


class HBnBFacade:
    """
    Facade — single entry point between API and persistence layers.
    Now uses SQLAlchemyRepository (Task 5 & 6).
    """

    def __init__(self):
        self.user_repo    = SQLAlchemyRepository(User)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo   = SQLAlchemyRepository(Place)
        self.review_repo  = SQLAlchemyRepository(Review)

    # ================================================================== #
    #  USER
    # ================================================================== #

    def create_user(self, data):
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            is_admin=data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email.lower().strip() if email else '')

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        # If password provided, hash it
        if 'password' in data:
            user.hash_password(data.pop('password'))
            db.session.commit()
        user.update(data)
        return user

    # ================================================================== #
    #  AMENITY
    # ================================================================== #

    def create_amenity(self, data):
        amenity = Amenity(name=data['name'])
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
        amenity.update(data)
        return amenity

    # ================================================================== #
    #  PLACE
    # ================================================================== #

    def create_place(self, data):
        owner = self.user_repo.get(data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner_id=data['owner_id']
        )
        for amenity_id in data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
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
            place.amenities = []
            for aid in amenity_ids:
                a = self.amenity_repo.get(aid)
                if a:
                    place.amenities.append(a)
            db.session.commit()
        place.update(data)
        return place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True

    # ================================================================== #
    #  REVIEW
    # ================================================================== #

    def create_review(self, data):
        user = self.user_repo.get(data.get('user_id'))
        if not user:
            raise ValueError("User not found")
        place = self.place_repo.get(data.get('place_id'))
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=data['text'],
            rating=data['rating'],
            place_id=data['place_id'],
            user_id=data['user_id']
        )
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
        review.update(data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True


facade = HBnBFacade()
