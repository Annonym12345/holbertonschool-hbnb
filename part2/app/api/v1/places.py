"""Endpoints Places — /api/v1/places/

Routes :
  GET    /api/v1/places/                → liste tous les logements
  POST   /api/v1/places/                → crée un logement
  GET    /api/v1/places/<id>            → récupère un logement (+ owner + amenities)
  PUT    /api/v1/places/<id>            → modifie un logement
  GET    /api/v1/places/<id>/reviews    → liste les avis du logement

Particularités :
  - La réponse inclut les détails du owner (first_name, last_name, email)
  - La réponse inclut la liste complète des amenities
  - Validation : price >= 0, latitude ∈ [-90,90], longitude ∈ [-180,180]

Note : DELETE non implémenté en Part 2.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

ns = Namespace('places', description='Opérations sur les logements')

# ── Modèles Swagger ──────────────────────────────────────────────────────────

place_input_model = ns.model('PlaceInput', {
    'title':       fields.String(required=True,  description='Titre du logement'),
    'description': fields.String(required=False, description='Description'),
    'price':       fields.Float(required=True,   description='Prix par nuit (>= 0)'),
    'latitude':    fields.Float(required=True,   description='Latitude (-90 à 90)'),
    'longitude':   fields.Float(required=True,   description='Longitude (-180 à 180)'),
    'owner_id':    fields.String(required=True,  description='UUID du propriétaire'),
    'amenities':   fields.List(fields.String,    description='Liste d\'UUIDs d\'amenities'),
})

place_update_model = ns.model('PlaceUpdate', {
    'title':       fields.String(description='Titre'),
    'description': fields.String(description='Description'),
    'price':       fields.Float(description='Prix par nuit'),
    'latitude':    fields.Float(description='Latitude'),
    'longitude':   fields.Float(description='Longitude'),
    'amenities':   fields.List(fields.String, description='UUIDs amenities'),
})

# Modèles imbriqués pour la réponse enrichie
owner_nested = ns.model('OwnerNested', {
    'id':         fields.String(description='UUID du owner'),
    'first_name': fields.String(description='Prénom'),
    'last_name':  fields.String(description='Nom'),
    'email':      fields.String(description='Email'),
})

amenity_nested = ns.model('AmenityNested', {
    'id':   fields.String(description='UUID'),
    'name': fields.String(description='Nom'),
})

place_output_model = ns.model('PlaceOutput', {
    'id':          fields.String(description='UUID'),
    'title':       fields.String(description='Titre'),
    'description': fields.String(description='Description'),
    'price':       fields.Float(description='Prix par nuit'),
    'latitude':    fields.Float(description='Latitude'),
    'longitude':   fields.Float(description='Longitude'),
    'owner_id':    fields.String(description='UUID du owner'),
    'owner':       fields.Nested(owner_nested,   description='Détails du propriétaire'),
    'amenities':   fields.List(fields.Nested(amenity_nested), description='Équipements'),
    'created_at':  fields.String(description='Date de création'),
    'updated_at':  fields.String(description='Date de modification'),
})

# ── Helpers ───────────────────────────────────────────────────────────────────

def _enrich(place) -> dict:
    """Enrichit le dict du place avec owner et amenities."""
    data = place.to_dict()

    owner = facade.get_user(place.owner_id)
    data['owner'] = {
        'id':         owner.id,
        'first_name': owner.first_name,
        'last_name':  owner.last_name,
        'email':      owner.email,
    } if owner else {}

    data['amenities'] = [a.to_dict() for a in place.amenities]
    return data

# ── Ressources ────────────────────────────────────────────────────────────────

@ns.route('/')
class PlaceList(Resource):

    @ns.doc('list_places')
    def get(self):
        """Retourne tous les logements avec owner et amenities."""
        return [_enrich(p) for p in facade.get_all_places()], 200

    @ns.doc('create_place')
    @ns.expect(place_input_model, validate=True)
    def post(self):
        """Crée un nouveau logement."""
        try:
            place = facade.create_place(dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        return _enrich(place), 201


@ns.route('/<string:place_id>')
@ns.response(404, 'Logement introuvable')
class PlaceResource(Resource):

    @ns.doc('get_place')
    def get(self, place_id):
        """Retourne un logement par son id (avec owner et amenities)."""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, 'Logement introuvable')
        return _enrich(place), 200

    @ns.doc('update_place')
    @ns.expect(place_update_model, validate=True)
    def put(self, place_id):
        """Met à jour un logement."""
        try:
            place = facade.update_place(place_id, dict(ns.payload))
        except ValueError as e:
            ns.abort(400, str(e))
        if not place:
            ns.abort(404, 'Logement introuvable')
        return _enrich(place), 200


@ns.route('/<string:place_id>/reviews')
@ns.response(404, 'Logement introuvable')
class PlaceReviews(Resource):

    @ns.doc('get_place_reviews')
    def get(self, place_id):
        """Retourne tous les avis d'un logement."""
        if not facade.get_place(place_id):
            ns.abort(404, 'Logement introuvable')
        return [r.to_dict() for r in facade.get_reviews_by_place(place_id)], 200
