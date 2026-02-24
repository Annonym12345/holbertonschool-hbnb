"""Tests unitaires et tests API pour le projet HBnB Part 2.

Lancer avec :
    python test_models.py
    # ou avec pytest :
    python -m pytest test_models.py -v

Couverture :
    - TestModels  : validation des modèles (User, Amenity, Place, Review)
    - TestFacade  : logique métier via la façade
    - TestAPI     : tests black-box des endpoints REST
"""

import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade


# ═══════════════════════════════════════════════════════════ TESTS MODÈLES

class TestModels(unittest.TestCase):
    """Valide les règles de validation des entités métier."""

    # ── User ──────────────────────────────────────────────────────────────

    def test_user_valide(self):
        from app.models.user import User
        u = User('Alice', 'Dupont', 'alice@test.com', 'motdepasse')
        self.assertEqual(u.first_name, 'Alice')
        self.assertIsNotNone(u.id)
        self.assertIsNotNone(u.created_at)

    def test_user_email_invalide(self):
        from app.models.user import User
        with self.assertRaises(ValueError):
            User('Alice', 'Dupont', 'pas-un-email', 'pwd')

    def test_user_prenom_vide(self):
        from app.models.user import User
        with self.assertRaises(ValueError):
            User('', 'Dupont', 'alice@test.com', 'pwd')

    def test_user_prenom_trop_long(self):
        from app.models.user import User
        with self.assertRaises(ValueError):
            User('A' * 51, 'Dupont', 'alice@test.com', 'pwd')

    def test_user_mdp_vide(self):
        from app.models.user import User
        with self.assertRaises(ValueError):
            User('Alice', 'Dupont', 'alice@test.com', '')

    # ── Amenity ───────────────────────────────────────────────────────────

    def test_amenity_valide(self):
        from app.models.amenity import Amenity
        a = Amenity('WiFi')
        self.assertEqual(a.name, 'WiFi')

    def test_amenity_nom_vide(self):
        from app.models.amenity import Amenity
        with self.assertRaises(ValueError):
            Amenity('')

    def test_amenity_nom_trop_long(self):
        from app.models.amenity import Amenity
        with self.assertRaises(ValueError):
            Amenity('X' * 51)

    # ── Place ─────────────────────────────────────────────────────────────

    def test_place_valide(self):
        from app.models.place import Place
        p = Place('Bel appart', 'Super vue', 80.0, 48.8566, 2.3522, 'owner-id')
        self.assertEqual(p.title, 'Bel appart')
        self.assertEqual(p.price, 80.0)

    def test_place_prix_negatif(self):
        from app.models.place import Place
        with self.assertRaises(ValueError):
            Place('Flat', '', -10, 48.8, 2.3, 'owner-id')

    def test_place_latitude_invalide(self):
        from app.models.place import Place
        with self.assertRaises(ValueError):
            Place('Flat', '', 50, 91.0, 2.3, 'owner-id')

    def test_place_longitude_invalide(self):
        from app.models.place import Place
        with self.assertRaises(ValueError):
            Place('Flat', '', 50, 48.0, 181.0, 'owner-id')

    def test_place_sans_owner(self):
        from app.models.place import Place
        with self.assertRaises(ValueError):
            Place('Flat', '', 50, 48.0, 2.0, '')

    # ── Review ────────────────────────────────────────────────────────────

    def test_review_valide(self):
        from app.models.review import Review
        r = Review('Super séjour !', 5, 'place-id', 'user-id')
        self.assertEqual(r.rating, 5)

    def test_review_note_trop_haute(self):
        from app.models.review import Review
        with self.assertRaises(ValueError):
            Review('Bien', 6, 'place-id', 'user-id')

    def test_review_note_trop_basse(self):
        from app.models.review import Review
        with self.assertRaises(ValueError):
            Review('Nul', 0, 'place-id', 'user-id')

    def test_review_texte_vide(self):
        from app.models.review import Review
        with self.assertRaises(ValueError):
            Review('', 3, 'place-id', 'user-id')


# ══════════════════════════════════════════════════════════════ TESTS FAÇADE

class TestFacade(unittest.TestCase):
    """Valide la logique métier via la façade."""

    def setUp(self):
        self.f = HBnBFacade()

    def _user(self, email='bob@test.com'):
        return self.f.create_user({
            'first_name': 'Bob', 'last_name': 'Martin',
            'email': email, 'password': 'secret'
        })

    def _place(self, owner_id):
        return self.f.create_place({
            'title': 'Loft', 'description': 'Cool',
            'price': 60, 'latitude': 10, 'longitude': 20,
            'owner_id': owner_id
        })

    def test_create_et_get_user(self):
        user = self._user()
        found = self.f.get_user(user.id)
        self.assertEqual(found.email, 'bob@test.com')

    def test_email_duplique_leve_erreur(self):
        self._user()
        with self.assertRaises(ValueError):
            self._user()  # même email

    def test_update_user(self):
        user = self._user()
        self.f.update_user(user.id, {'first_name': 'Bobby'})
        self.assertEqual(self.f.get_user(user.id).first_name, 'Bobby')

    def test_create_place_owner_inexistant(self):
        with self.assertRaises(ValueError):
            self.f.create_place({
                'title': 'Flat', 'description': '',
                'price': 50, 'latitude': 10, 'longitude': 10,
                'owner_id': 'faux-id'
            })

    def test_create_et_delete_review(self):
        user = self._user()
        place = self._place(user.id)
        review = self.f.create_review({
            'text': 'Parfait !', 'rating': 5,
            'place_id': place.id, 'user_id': user.id
        })
        self.assertIsNotNone(self.f.get_review(review.id))
        self.assertTrue(self.f.delete_review(review.id))
        self.assertIsNone(self.f.get_review(review.id))

    def test_delete_review_retire_du_place(self):
        user = self._user()
        place = self._place(user.id)
        review = self.f.create_review({
            'text': 'Top', 'rating': 4,
            'place_id': place.id, 'user_id': user.id
        })
        self.assertEqual(len(place.reviews), 1)
        self.f.delete_review(review.id)
        self.assertEqual(len(place.reviews), 0)

    def test_reviews_by_place(self):
        user = self._user()
        place = self._place(user.id)
        self.f.create_review({'text': 'A', 'rating': 3,
                               'place_id': place.id, 'user_id': user.id})
        self.f.create_review({'text': 'B', 'rating': 4,
                               'place_id': place.id, 'user_id': user.id})
        self.assertEqual(len(self.f.get_reviews_by_place(place.id)), 2)


# ═══════════════════════════════════════════════════════════════ TESTS API

class TestAPI(unittest.TestCase):
    """Tests black-box des endpoints REST."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def _post(self, url, data):
        return self.client.post(
            url, data=json.dumps(data), content_type='application/json'
        )

    def _put(self, url, data):
        return self.client.put(
            url, data=json.dumps(data), content_type='application/json'
        )

    def _new_user(self, email):
        r = self._post('/api/v1/users/', {
            'first_name': 'Test', 'last_name': 'User',
            'email': email, 'password': 'pw'
        })
        return json.loads(r.data)['id']

    # ── Users ─────────────────────────────────────────────────────────────

    def test_creer_user_201(self):
        r = self._post('/api/v1/users/', {
            'first_name': 'Lena', 'last_name': 'K',
            'email': 'lena@test.com', 'password': 'pw'
        })
        self.assertEqual(r.status_code, 201)
        body = json.loads(r.data)
        # Le password ne doit jamais apparaître
        self.assertNotIn('password', body)
        self.assertIn('id', body)

    def test_email_duplique_400(self):
        data = {'first_name': 'X', 'last_name': 'Y',
                'email': 'dup@test.com', 'password': 'pw'}
        self._post('/api/v1/users/', data)
        r = self._post('/api/v1/users/', data)
        self.assertEqual(r.status_code, 400)

    def test_get_user_404(self):
        r = self.client.get('/api/v1/users/id-inexistant')
        self.assertEqual(r.status_code, 404)

    def test_get_liste_users_200(self):
        self._new_user('list1@test.com')
        r = self.client.get('/api/v1/users/')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(json.loads(r.data), list)

    def test_update_user_200(self):
        uid = self._new_user('update@test.com')
        r = self._put(f'/api/v1/users/{uid}', {'first_name': 'NewName'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data)['first_name'], 'NewName')

    # ── Amenities ─────────────────────────────────────────────────────────

    def test_creer_amenity_201(self):
        r = self._post('/api/v1/amenities/', {'name': 'Piscine'})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data)['name'], 'Piscine')

    def test_amenity_nom_vide_400(self):
        r = self._post('/api/v1/amenities/', {'name': ''})
        self.assertEqual(r.status_code, 400)

    def test_get_amenity_404(self):
        r = self.client.get('/api/v1/amenities/faux-id')
        self.assertEqual(r.status_code, 404)

    # ── Places ────────────────────────────────────────────────────────────

    def test_creer_place_201(self):
        uid = self._new_user('owner@test.com')
        r = self._post('/api/v1/places/', {
            'title': 'Studio Paris', 'description': 'Sympa',
            'price': 99.0, 'latitude': 48.8566, 'longitude': 2.3522,
            'owner_id': uid
        })
        self.assertEqual(r.status_code, 201)
        body = json.loads(r.data)
        # La réponse doit contenir les détails du owner
        self.assertIn('owner', body)
        self.assertEqual(body['owner']['id'], uid)
        # La réponse doit contenir la liste des amenities
        self.assertIn('amenities', body)

    def test_place_owner_inexistant_400(self):
        r = self._post('/api/v1/places/', {
            'title': 'Flat', 'description': '',
            'price': 50, 'latitude': 10, 'longitude': 10,
            'owner_id': 'faux-id'
        })
        self.assertEqual(r.status_code, 400)

    def test_place_prix_negatif_400(self):
        uid = self._new_user('owner2@test.com')
        r = self._post('/api/v1/places/', {
            'title': 'Flat', 'description': '',
            'price': -5, 'latitude': 10, 'longitude': 10,
            'owner_id': uid
        })
        self.assertEqual(r.status_code, 400)

    def test_get_place_404(self):
        r = self.client.get('/api/v1/places/faux-id')
        self.assertEqual(r.status_code, 404)

    # ── Reviews ───────────────────────────────────────────────────────────

    def _setup_place(self, email):
        uid = self._new_user(email)
        r = self._post('/api/v1/places/', {
            'title': 'Appart', 'description': '',
            'price': 60, 'latitude': 10, 'longitude': 20,
            'owner_id': uid
        })
        pid = json.loads(r.data)['id']
        return uid, pid

    def test_creer_et_supprimer_review(self):
        uid, pid = self._setup_place('rev1@test.com')
        r = self._post('/api/v1/reviews/', {
            'text': 'Génial !', 'rating': 5,
            'place_id': pid, 'user_id': uid
        })
        self.assertEqual(r.status_code, 201)
        rid = json.loads(r.data)['id']

        # DELETE
        d = self.client.delete(f'/api/v1/reviews/{rid}')
        self.assertEqual(d.status_code, 200)

        # GET après delete → 404
        g = self.client.get(f'/api/v1/reviews/{rid}')
        self.assertEqual(g.status_code, 404)

    def test_review_note_invalide_400(self):
        uid, pid = self._setup_place('rev2@test.com')
        r = self._post('/api/v1/reviews/', {
            'text': 'Mouais', 'rating': 10,
            'place_id': pid, 'user_id': uid
        })
        self.assertEqual(r.status_code, 400)

    def test_review_user_inexistant_400(self):
        uid, pid = self._setup_place('rev3@test.com')
        r = self._post('/api/v1/reviews/', {
            'text': 'Super', 'rating': 4,
            'place_id': pid, 'user_id': 'faux-id'
        })
        self.assertEqual(r.status_code, 400)

    def test_place_reviews_endpoint(self):
        uid, pid = self._setup_place('rev4@test.com')
        self._post('/api/v1/reviews/', {
            'text': 'Top', 'rating': 5,
            'place_id': pid, 'user_id': uid
        })
        r = self.client.get(f'/api/v1/places/{pid}/reviews')
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]['rating'], 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
