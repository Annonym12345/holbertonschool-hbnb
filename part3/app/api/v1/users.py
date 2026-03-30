"""
Tasks 3 & 4 — User endpoints with JWT protection and admin access.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name':  fields.String(required=True),
    'email':      fields.String(required=True),
    'password':   fields.String(required=True, description='Min 6 characters')
})

user_response = api.model('UserResponse', {
    'id':         fields.String(),
    'first_name': fields.String(),
    'last_name':  fields.String(),
    'email':      fields.String(),
    'is_admin':   fields.Boolean(),
    'created_at': fields.String(),
    'updated_at': fields.String()
})


@api.route('/')
class UserList(Resource):

    @api.response(200, 'List of users')
    def get(self):
        """Public — list all users (password excluded)."""
        return [u.to_dict() for u in facade.get_all_users()], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Validation error')
    @api.response(403, 'Admin only')
    @jwt_required(optional=True)   # Task 4: admin creates users; public self-register also allowed
    def post(self):
        """Create a new user (admin) or self-register (public)."""
        claims   = get_jwt()
        is_admin = claims.get('is_admin', False)
        data     = api.payload

        # Only admins can set is_admin flag
        if data.get('is_admin', False) and not is_admin:
            return {'error': 'Admin privileges required to create admin users'}, 403

        if facade.get_user_by_email(data.get('email')):
            return {'error': 'Email already registered'}, 400
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:user_id>')
class UserResource(Resource):

    @api.response(200, 'User details')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Public — get user by ID (password excluded)."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """
        Task 3: authenticated users can update their own profile (no email/password change).
        Task 4: admins can update any user including email and password.
        """
        current_user_id = get_jwt_identity()
        claims          = get_jwt()
        is_admin        = claims.get('is_admin', False)
        data            = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not is_admin and current_user_id != user_id:
            return {'error': 'You can only modify your own data'}, 403

        # Task 3: regular users cannot change email or password
        if not is_admin:
            data.pop('email',    None)
            data.pop('password', None)
            data.pop('is_admin', None)

        # Task 4: admins can change email — check uniqueness
        if is_admin and 'email' in data and data['email'] != user.email:
            if facade.get_user_by_email(data['email']):
                return {'error': 'Email already registered'}, 400

        try:
            updated = facade.update_user(user_id, data)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
