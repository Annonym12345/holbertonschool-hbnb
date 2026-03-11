from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import app.services.facade as facade_module

ns = Namespace('places', description='Place operations')

def _f():
    return facade_module.facade

place_input_model = ns.model('PlaceInput', {
    'title':       fields.String(required=True),
    'description': fields.String(),
    'price':       fields.Float(required=True),
    'latitude':    fields.Float(required=True),
    'longitude':   fields.Float(required=True),
    'owner_id':    fields.String(required=True),
    'amenities':   fields.List(fields.String),
})
place_update_model = ns.model('PlaceUpdate', {
    'title': fields.String(), 'description': fields.String(),
    'price': fields.Float(),  'latitude': fields.Float(),
    'longitude': fields.Float(), 'amenities': fields.List(fields.String),
})

def _enrich(place):
    data  = place.to_dict()
    owner = _f().get_user(place.owner_id)
    data['owner'] = {
        'id': owner.id, 'first_name': owner.first_name,
        'last_name': owner.last_name, 'email': owner.email,
    } if owner else {}
    data['amenities'] = [a.to_dict() for a in place.amenities]
    return data

@ns.route('/')
class PlaceList(Resource):
    def get(self):
        return [_enrich(p) for p in _f().get_all_places()], 200

    @jwt_required()
    def post(self):
        try:
            place = _f().create_place(dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return _enrich(place), 201

@ns.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = _f().get_place(place_id)
        if not place:
            ns.abort(404, 'Place not found')
        return _enrich(place), 200

    @jwt_required()
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        place = _f().get_place(place_id)
        if not place:
            ns.abort(404, 'Place not found')
        if not is_admin and place.owner_id != current_user_id:
            ns.abort(403, 'Unauthorized action')
        try:
            place = _f().update_place(place_id, dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return _enrich(place), 200

@ns.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        if not _f().get_place(place_id):
            ns.abort(404, 'Place not found')
        return [r.to_dict() for r in _f().get_reviews_by_place(place_id)], 200
