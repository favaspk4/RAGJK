from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()
jwt = JWTManager()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/flask_rag_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def init_auth(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
    jwt.init_app(app)