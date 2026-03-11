from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    import app.services.facade as facade_module
    from app.services.facade import HBnBFacade
    facade_module.facade = HBnBFacade()

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API — Part 3', doc='/api/v1/')

    from app.api.v1.namespaces.users     import ns as users_ns
    from app.api.v1.namespaces.amenities import ns as amenities_ns
    from app.api.v1.namespaces.places    import ns as places_ns
    from app.api.v1.namespaces.reviews   import ns as reviews_ns
    from app.api.v1.namespaces.auth      import ns as auth_ns

    api.add_namespace(auth_ns,      path='/api/v1/auth')
    api.add_namespace(users_ns,     path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns,    path='/api/v1/places')
    api.add_namespace(reviews_ns,   path='/api/v1/reviews')

    return app
