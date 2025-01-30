from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.utils import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, editor, viewer

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)  # Store file path or S3 URL
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Embedding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    embedding = db.Column(db.Text, nullable=False)  # Store embeddings as JSON