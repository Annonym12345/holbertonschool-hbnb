from flask import Flask, render_template, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db     = SQLAlchemy()
bcrypt = Bcrypt()
jwt    = JWTManager()


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

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/v1')
    def v1_redirect():
        return redirect('/api/v1/')

    # Inject login button into Swagger UI via after_request
    @app.after_request
    def inject_login_button(response):
        if response.content_type == 'text/html; charset=utf-8':
            btn = b'''
            <style>
              .login-btn {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #7F77DD;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                text-decoration: none;
                position: fixed;
                top: 16px;
                right: 24px;
                z-index: 9999;
              }
              .login-btn:hover { background: #6b63cc; }
            </style>
            <a href="/login" class="login-btn">
              <svg width="16" height="16" viewBox="0 0 52 52" fill="none">
                <rect x="10" y="24" width="32" height="22" rx="5" fill="white"/>
                <path d="M17 24V18a9 9 0 0 1 18 0v6" stroke="white" stroke-width="3.5" stroke-linecap="round" fill="none"/>
                <circle cx="26" cy="34" r="3" fill="#7F77DD"/>
                <line x1="26" y1="36" x2="26" y2="41" stroke="#7F77DD" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
              Login
            </a>
            '''
            response.data = response.data.replace(b'</body>', btn + b'</body>')
        return response

    return app
