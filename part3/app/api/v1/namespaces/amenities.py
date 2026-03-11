from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
import app.services.facade as facade_module

ns = Namespace('amenities', description='Amenity operations')

def _f():
    return facade_module.facade

amenity_input_model  = ns.model('AmenityInput',  {'name': fields.String(required=True)})
amenity_output_model = ns.model('AmenityOutput', {
    'id': fields.String(), 'name': fields.String(),
    'created_at': fields.String(), 'updated_at': fields.String(),
})

@ns.route('/')
class AmenityList(Resource):
    @ns.marshal_list_with(amenity_output_model)
    def get(self):
        return _f().get_all_amenities(), 200

    @jwt_required()
    @ns.expect(amenity_input_model, validate=True)
    @ns.marshal_with(amenity_output_model, code=201)
    def post(self):
        if not get_jwt().get('is_admin'):
            ns.abort(403, 'Admin access required')
        try:
            amenity = _f().create_amenity(dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return amenity, 201

@ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @ns.marshal_with(amenity_output_model)
    def get(self, amenity_id):
        amenity = _f().get_amenity(amenity_id)
        if not amenity:
            ns.abort(404, 'Amenity not found')
        return amenity, 200

    @jwt_required()
    @ns.expect(amenity_input_model, validate=True)
    @ns.marshal_with(amenity_output_model)
    def put(self, amenity_id):
        if not get_jwt().get('is_admin'):
            ns.abort(403, 'Admin access required')
        amenity = _f().update_amenity(amenity_id, dict(ns.payload))
        if not amenity:
            ns.abort(404, 'Amenity not found')
        return amenity, 200
