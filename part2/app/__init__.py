from flask import Flask


def create_app(config_name=None):
    app = Flask(__name__)

    # Isolation de la facade en mode testing
    # (chaque test repart d'un stockage vide)
    import app.services.facade as facade_module
    from app.services.facade import HBnBFacade
    facade_module.facade = HBnBFacade()

    try:
        from flask_restx import Api

        api = Api(
            app,
            version='1.0',
            title='HBnB API',
            description='HBnB Application API',
            doc='/api/v1/'
        )

        from app.api.v1.namespaces.users import ns as users_ns
        from app.api.v1.namespaces.amenities import ns as amenities_ns
        from app.api.v1.namespaces.places import ns as places_ns
        from app.api.v1.namespaces.reviews import ns as reviews_ns

        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')

    except ImportError:
        from app.api.v1.fallback import bp
        app.register_blueprint(bp, url_prefix='/api/v1')

    return app
