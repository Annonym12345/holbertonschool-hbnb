"""Endpoints Reviews — /api/v1/reviews/

Routes :
  GET    /api/v1/reviews/        → liste tous les avis
  POST   /api/v1/reviews/        → crée un avis
  GET    /api/v1/reviews/<id>    → récupère un avis par id
  PUT    /api/v1/reviews/<id>    → modifie un avis
  DELETE /api/v1/reviews/<id>    → supprime un avis ← seule entité avec DELETE en Part 2
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

ns = Namespace('reviews', description='Opérations sur les avis')

# ── Modèles Swagger ──────────────────────────────────────────────────────────

review_input_model = ns.model('ReviewInput', {
    'text':     fields.String(required=True,  description='Texte de l\'avis'),
    'rating':   fields.Integer(required=True, description='Note de 1 à 5'),
    'place_id': fields.String(required=True,  description='UUID du logement'),
    'user_id':  fields.String(required=True,  description='UUID de l\'auteur'),
})

review_update_model = ns.model('ReviewUpdate', {
    'text':   fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note de 1 à 5'),
})

review_output_model = ns.model('ReviewOutput', {
    'id':         fields.String(description='UUID'),
    'text':       fields.String(description='Texte'),
    'rating':     fields.Integer(description='Note'),
    'place_id':   fields.String(description='UUID du logement'),
    'user_id':    fields.String(description='UUID de l\'auteur'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de modification'),
})

# ── Ressources ────────────────────────────────────────────────────────────────

@ns.route('/')
class ReviewList(Resource):

    @ns.doc('list_reviews')
    @ns.marshal_list_with(review_output_model)
    def get(self):
        """Retourne tous les avis."""
        return facade.get_all_reviews(), 200

    @ns.doc('create_review')
    @ns.expect(review_input_model, validate=True)
    @ns.marshal_with(review_output_model, code=201)
    def post(self):
        """Crée un nouvel avis."""
        try:
            review = facade.create_review(ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))
        return review, 201


@ns.route('/<string:review_id>')
@ns.response(404, 'Avis introuvable')
class ReviewResource(Resource):

    @ns.doc('get_review')
    @ns.marshal_with(review_output_model)
    def get(self, review_id):
        """Retourne un avis par son id."""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, 'Avis introuvable')
        return review, 200

    @ns.doc('update_review')
    @ns.expect(review_update_model, validate=True)
    @ns.marshal_with(review_output_model)
    def put(self, review_id):
        """Met à jour un avis."""
        try:
            review = facade.update_review(review_id, ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))
        if not review:
            ns.abort(404, 'Avis introuvable')
        return review, 200

    @ns.doc('delete_review')
    @ns.response(200, 'Avis supprimé')
    def delete(self, review_id):
        """Supprime un avis (seule opération DELETE disponible en Part 2)."""
        if not facade.delete_review(review_id):
            ns.abort(404, 'Avis introuvable')
        return {'message': 'Avis supprimé avec succès'}, 200
