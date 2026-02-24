"""Endpoints Amenities — /api/v1/amenities/

Routes :
  GET    /api/v1/amenities/       → liste tous les équipements
  POST   /api/v1/amenities/       → crée un équipement
  GET    /api/v1/amenities/<id>   → récupère un équipement par id
  PUT    /api/v1/amenities/<id>   → modifie un équipement

Note : DELETE non implémenté en Part 2.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

ns = Namespace('amenities', description='Opérations sur les équipements')

# ── Modèles Swagger ──────────────────────────────────────────────────────────

amenity_input_model = ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Nom de l\'équipement'),
})

amenity_output_model = ns.model('AmenityOutput', {
    'id':         fields.String(description='UUID'),
    'name':       fields.String(description='Nom'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de modification'),
})

# ── Ressources ────────────────────────────────────────────────────────────────

@ns.route('/')
class AmenityList(Resource):

    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_output_model)
    def get(self):
        """Retourne la liste de tous les équipements."""
        return facade.get_all_amenities(), 200

    @ns.doc('create_amenity')
    @ns.expect(amenity_input_model, validate=True)
    @ns.marshal_with(amenity_output_model, code=201)
    def post(self):
        """Crée un nouvel équipement."""
        try:
            amenity = facade.create_amenity(ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))
        return amenity, 201


@ns.route('/<string:amenity_id>')
@ns.response(404, 'Équipement introuvable')
class AmenityResource(Resource):

    @ns.doc('get_amenity')
    @ns.marshal_with(amenity_output_model)
    def get(self, amenity_id):
        """Retourne un équipement par son id."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            ns.abort(404, 'Équipement introuvable')
        return amenity, 200

    @ns.doc('update_amenity')
    @ns.expect(amenity_input_model, validate=True)
    @ns.marshal_with(amenity_output_model)
    def put(self, amenity_id):
        """Met à jour un équipement."""
        amenity = facade.update_amenity(amenity_id, ns.payload)
        if not amenity:
            ns.abort(404, 'Équipement introuvable')
        return amenity, 200
