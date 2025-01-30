from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import AuthService, DocumentService

def init_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        return AuthService.register(data)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        return AuthService.login(data)

    @app.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        return AuthService.logout()

    @app.route('/upload', methods=['POST'])
    @jwt_required()
    def upload_document():
        data = request.get_json()
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']  # Associate the document with the logged-in user
        return DocumentService.upload_document(data)

    @app.route('/document/<int:document_id>', methods=['GET'])
    @jwt_required()
    def get_document(document_id):
        return DocumentService.get_document(document_id)