from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
import app.services.facade as facade_module

ns = Namespace('auth', description='Authentication')

def _f():
    return facade_module.facade

login_model = ns.model('Login', {
    'email':    fields.String(required=True),
    'password': fields.String(required=True),
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        """Login — returns JWT token."""
        user = _f().get_user_by_email(ns.payload.get('email'))
        if not user or not user.verify_password(ns.payload.get('password')):
            ns.abort(401, 'Invalid credentials')
        token = create_access_token(
            identity=user.id,
            additional_claims={'is_admin': user.is_admin}
        )
        return {'access_token': token}, 200
