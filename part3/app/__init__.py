from flask import Flask, render_template, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db     = SQLAlchemy()
bcrypt = Bcrypt()
jwt    = JWTManager()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: **Bearer &lt;your_token&gt;**'
    }
}


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API — Part 3',
        authorizations=authorizations,
        security='Bearer Auth',
        doc='/api/v1/'
    )

    from app.api.v1.users     import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places    import api as places_ns
    from app.api.v1.reviews   import api as reviews_ns
    from app.api.v1.auth      import api as auth_ns

    api.add_namespace(users_ns,     path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns,    path='/api/v1/places')
    api.add_namespace(reviews_ns,   path='/api/v1/reviews')
    api.add_namespace(auth_ns,      path='/api/v1/auth')

    with app.app_context():
        db.create_all()

    @app.route('/v1')
    def v1_redirect():
        return redirect('/api/v1/')

    return app
