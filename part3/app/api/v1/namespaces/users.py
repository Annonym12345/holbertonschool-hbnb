from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import app.services.facade as facade_module

ns = Namespace('users', description='User operations')

def _f():
    return facade_module.facade

user_input_model = ns.model('UserInput', {
    'first_name': fields.String(required=True),
    'last_name':  fields.String(required=True),
    'email':      fields.String(required=True),
    'password':   fields.String(required=True),
})
user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(),
    'last_name':  fields.String(),
    'email':      fields.String(),
    'password':   fields.String(),
})
user_output_model = ns.model('UserOutput', {
    'id':         fields.String(),
    'first_name': fields.String(),
    'last_name':  fields.String(),
    'email':      fields.String(),
    'is_admin':   fields.Boolean(),
    'created_at': fields.String(),
    'updated_at': fields.String(),
})

@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_output_model)
    def get(self):
        return _f().get_all_users(), 200

    @jwt_required()
    @ns.expect(user_input_model, validate=True)
    @ns.marshal_with(user_output_model, code=201)
    def post(self):
        if not get_jwt().get('is_admin'):
            ns.abort(403, 'Admin access required')
        try:
            user = _f().create_user(dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return user, 201

@ns.route('/<string:user_id>')
class UserResource(Resource):
    @ns.marshal_with(user_output_model)
    def get(self, user_id):
        user = _f().get_user(user_id)
        if not user:
            ns.abort(404, 'User not found')
        return user, 200

    @jwt_required()
    @ns.expect(user_update_model, validate=True)
    @ns.marshal_with(user_output_model)
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and current_user_id != user_id:
            ns.abort(403, 'Unauthorized action')
        try:
            user = _f().update_user(user_id, dict(ns.payload), is_admin=is_admin)
        except ValueError as e:
            ns.abort(400, str(e))
        if not user:
            ns.abort(404, 'User not found')
        return user, 200
