"""
Task 3 & 4 — Review endpoints with ownership, duplicate and self-review checks.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.review import Review
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text':     fields.String(required=True),
    'rating':   fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

review_response = api.model('ReviewResponse', {
    'id':         fields.String(),
    'text':       fields.String(),
    'rating':     fields.Integer(),
    'place_id':   fields.String(),
    'user_id':    fields.String(),
    'created_at': fields.String(),
    'updated_at': fields.String()
})


@api.route('/')
class ReviewList(Resource):

    def get(self):
        """Public — list all reviews."""
        return [r.to_dict() for r in facade.get_all_reviews()], 200

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created')
    @api.response(400, 'Validation / business-rule error')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """
        Task 3: authenticated — create a review.
        Business rules:
          - Cannot review own place.
          - Cannot review the same place twice.
        """
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)
        data            = api.payload
        data['user_id'] = current_user_id

        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        # Task 3: cannot review own place (admins bypass)
        if not is_admin and place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        # Task 3: duplicate review check
        existing = Review.query.filter_by(
            place_id=data['place_id'], user_id=current_user_id
        ).first()
        if existing and not is_admin:
            return {'error': 'You have already reviewed this place'}, 400

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Public — get review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Task 3: author can update; Task 4: admin can update any."""
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'You can only modify your own reviews'}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Task 3: author can delete; Task 4: admin can delete any."""
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'You can only delete your own reviews'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Public — get all reviews for a place."""
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        return [r.to_dict() for r in facade.get_reviews_by_place(place_id)], 200
