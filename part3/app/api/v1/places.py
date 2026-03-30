"""
Task 3 & 4 — Place endpoints with ownership checks and admin bypass.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('places', description='Place operations')

amenity_nested = api.model('PlaceAmenity', {
    'id':   fields.String(),
    'name': fields.String()
})

owner_nested = api.model('PlaceOwner', {
    'id':         fields.String(),
    'first_name': fields.String(),
    'last_name':  fields.String(),
    'email':      fields.String()
})

place_model = api.model('Place', {
    'title':       fields.String(required=True),
    'description': fields.String(),
    'price':       fields.Float(required=True),
    'latitude':    fields.Float(required=True),
    'longitude':   fields.Float(required=True),
    'owner_id':    fields.String(required=True),
    'amenities':   fields.List(fields.String)
})


def _enrich(place):
    """Return place dict with owner details, amenities list and reviews."""
    data = place.to_dict()
    owner = facade.get_user(place.owner_id)
    data['owner'] = {
        'id': owner.id, 'first_name': owner.first_name,
        'last_name': owner.last_name, 'email': owner.email
    } if owner else None
    data['amenities'] = [{'id': a.id, 'name': a.name} for a in place.amenities]
    data['reviews']   = [
        {'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id}
        for r in place.reviews
    ]
    return data


@api.route('/')
class PlaceList(Resource):

    def get(self):
        """Public — list all places."""
        return [_enrich(p) for p in facade.get_all_places()], 200

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Validation error')
    @api.response(404, 'Owner not found')
    @jwt_required()
    def post(self):
        """Task 3: authenticated — create a place."""
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)
        data            = api.payload

        # Force owner_id to authenticated user unless admin
        if not is_admin:
            data['owner_id'] = current_user_id

        if not facade.get_user(data.get('owner_id')):
            return {'error': 'Owner not found'}, 404
        for aid in data.get('amenities', []):
            if not facade.get_amenity(aid):
                return {'error': f'Amenity {aid} not found'}, 404
        try:
            place = facade.create_place(data)
            return _enrich(place), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Public — get place by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return _enrich(place), 200

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Task 3: owner can update; Task 4: admin can update any."""
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'You can only modify your own places'}, 403

        for aid in api.payload.get('amenities', []):
            if not facade.get_amenity(aid):
                return {'error': f'Amenity {aid} not found'}, 404
        try:
            updated = facade.update_place(place_id, api.payload)
            return _enrich(updated), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Place deleted')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Task 3: owner can delete; Task 4: admin can delete any."""
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'You can only delete your own places'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
