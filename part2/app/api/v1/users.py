"""Endpoints Users — /api/v1/users/

Routes :
  GET    /api/v1/users/          → liste tous les users
  POST   /api/v1/users/          → crée un user
  GET    /api/v1/users/<id>      → récupère un user par id
  PUT    /api/v1/users/<id>      → modifie un user

Note : DELETE non implémenté en Part 2.
Note : le mot de passe n'apparaît JAMAIS dans les réponses.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

ns = Namespace('users', description='Opérations sur les utilisateurs')

# ── Modèles Swagger ──────────────────────────────────────────────────────────

user_input_model = ns.model('UserInput', {
    'first_name': fields.String(required=True,  description='Prénom'),
    'last_name':  fields.String(required=True,  description='Nom de famille'),
    'email':      fields.String(required=True,  description='Adresse email'),
    'password':   fields.String(required=True,  description='Mot de passe'),
})

user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(description='Prénom'),
    'last_name':  fields.String(description='Nom de famille'),
    'email':      fields.String(description='Adresse email'),
    'password':   fields.String(description='Mot de passe'),
})

user_output_model = ns.model('UserOutput', {
    'id':         fields.String(description='UUID'),
    'first_name': fields.String(description='Prénom'),
    'last_name':  fields.String(description='Nom de famille'),
    'email':      fields.String(description='Email'),
    'is_admin':   fields.Boolean(description='Admin ?'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de modification'),
})

# ── Ressources ────────────────────────────────────────────────────────────────

@ns.route('/')
class UserList(Resource):

    @ns.doc('list_users')
    @ns.marshal_list_with(user_output_model)
    def get(self):
        """Retourne la liste de tous les utilisateurs."""
        return facade.get_all_users(), 200

    @ns.doc('create_user')
    @ns.expect(user_input_model, validate=True)
    @ns.marshal_with(user_output_model, code=201)
    def post(self):
        """Crée un nouvel utilisateur."""
        try:
            user = facade.create_user(ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))
        return user, 201


@ns.route('/<string:user_id>')
@ns.response(404, 'Utilisateur introuvable')
class UserResource(Resource):

    @ns.doc('get_user')
    @ns.marshal_with(user_output_model)
    def get(self, user_id):
        """Retourne un utilisateur par son id."""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, 'Utilisateur introuvable')
        return user, 200

    @ns.doc('update_user')
    @ns.expect(user_update_model, validate=True)
    @ns.marshal_with(user_output_model)
    def put(self, user_id):
        """Met à jour les informations d'un utilisateur."""
        try:
            user = facade.update_user(user_id, ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))
        if not user:
            ns.abort(404, 'Utilisateur introuvable')
        return user, 200
