from flask import Flask
from .utils import init_db
from .utils  import init_auth
from app.routes import init_routes

def create_app():
    app = Flask(__name__)

    # Initialize database and authentication
    init_db(app)
    init_auth(app)

    # Register routes
    init_routes(app)

    return app