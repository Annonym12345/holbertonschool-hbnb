"""
Task 4 — Amenity endpoints: only admins can create/update.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

amenity_response = api.model('AmenityResponse', {
    'id':         fields.String(),
    'name':       fields.String(),
    'created_at': fields.String(),
    'updated_at': fields.String()
})


@api.route('/')
class AmenityList(Resource):

    @api.response(200, 'List of amenities')
    def get(self):
        """Public — list all amenities."""
        return [a.to_dict() for a in facade.get_all_amenities()], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created')
    @api.response(403, 'Admin only')
    @jwt_required()
    def post(self):
        """Task 4: admin only — create an amenity."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):

    @api.response(200, 'Amenity details')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Public — get amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated')
    @api.response(403, 'Admin only')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Task 4: admin only — update an amenity."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
