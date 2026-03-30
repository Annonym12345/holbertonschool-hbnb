"""
Task 2 — JWT Authentication endpoint.
POST /api/v1/auth/login  →  returns access_token
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('auth', description='Authentication')

login_model = api.model('Login', {
    'email':    fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})


@api.route('/login')
class Login(Resource):

    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate and receive a JWT token."""
        data  = api.payload
        user  = facade.get_user_by_email(data.get('email'))

        if not user or not user.verify_password(data.get('password', '')):
            return {'error': 'Invalid credentials'}, 401

        # Embed is_admin claim in the token — Task 2
        additional_claims = {'is_admin': user.is_admin}
        token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        return {'access_token': token}, 200
