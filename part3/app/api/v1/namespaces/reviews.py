from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import app.services.facade as facade_module

ns = Namespace('reviews', description='Review operations')

def _f():
    return facade_module.facade

review_input_model = ns.model('ReviewInput', {
    'text': fields.String(required=True), 'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True), 'user_id': fields.String(required=True),
})
review_update_model = ns.model('ReviewUpdate', {
    'text': fields.String(), 'rating': fields.Integer(),
})
review_output_model = ns.model('ReviewOutput', {
    'id': fields.String(), 'text': fields.String(), 'rating': fields.Integer(),
    'place_id': fields.String(), 'user_id': fields.String(),
    'created_at': fields.String(), 'updated_at': fields.String(),
})

@ns.route('/')
class ReviewList(Resource):
    @ns.marshal_list_with(review_output_model)
    def get(self):
        return _f().get_all_reviews(), 200

    @jwt_required()
    @ns.expect(review_input_model, validate=True)
    @ns.marshal_with(review_output_model, code=201)
    def post(self):
        current_user_id = get_jwt_identity()
        try:
            review = _f().create_review(dict(ns.payload), current_user_id)
        except ValueError as e:
            ns.abort(400, str(e))
        return review, 201

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    @ns.marshal_with(review_output_model)
    def get(self, review_id):
        review = _f().get_review(review_id)
        if not review:
            ns.abort(404, 'Review not found')
        return review, 200

    @jwt_required()
    @ns.expect(review_update_model, validate=True)
    @ns.marshal_with(review_output_model)
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        review = _f().get_review(review_id)
        if not review:
            ns.abort(404, 'Review not found')
        if not is_admin and review.user_id != current_user_id:
            ns.abort(403, 'Unauthorized action')
        try:
            review = _f().update_review(review_id, dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return review, 200

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        review = _f().get_review(review_id)
        if not review:
            ns.abort(404, 'Review not found')
        if not is_admin and review.user_id != current_user_id:
            ns.abort(403, 'Unauthorized action')
        _f().delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
