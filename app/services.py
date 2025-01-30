import os
from faker import Faker
from flask_jwt_extended import create_access_token
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from app.models import User, Document, db
from flask import current_app

fake = Faker()

class AuthService:
    @staticmethod
    def register(data):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is mandatory')
        parser.add_argument('password', type=str, required=True, help='password is mandatory')
        parser.add_argument('role', type=str, required=True, choices=['admin', 'staff', 'user'],
                            help='role is mandatory')
        args = parser.parse_args()

        existing_user = User.query.filter_by(username=args['username']).first()
        if existing_user:
            return {'message': 'username already exists'}, 400
        new_user = User(username=args['username'], role=args['role'])
        new_user.set_password(args['password'])

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User Registered Successfully'}, 201

    @staticmethod
    def login(data):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        existing_user = User.query.filter_by(username=args['username']).first()

        if existing_user and existing_user.check_password(args['password']):
            # expires=timedelta(minutes=10)
            # session['logged_in']=True

            # access_token = create_access_token(identity=existing_user.id, expires_delta=timedelta(minutes=10))
            access_token = create_access_token(identity=existing_user.role)

            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid Credentials'}, 401

    @staticmethod
    def logout():
        return {'message': 'User logged out successfully'}, 200


class DocumentService:
    @staticmethod
    def upload_document(file):
        """Uploads a document to the local filesystem or AWS S3"""
        if not file:
            return {"error": "No file provided"}, 400

        filename = secure_filename(file.filename)

        # LOCAL STORAGE: Save file to the local directory
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # STORE IN DATABASE
        new_document = Document(filename=filename, file_url=file_path)
        db.session.add(new_document)
        db.session.commit()

        return {"message": "File uploaded successfully", "document_id": new_document.id}, 201


    @staticmethod
    def get_document(document_id):
        """Retrieves a document's metadata"""
        document = Document.query.get(document_id)
        if not document:
            return {"error": "Document not found"}, 404

        return {
            "document_id": document.id,
            "filename": document.filename,
            "file_url": document.file_url,
            "uploaded_at": document.uploaded_at
        }, 200


class QAService:
    @staticmethod
    def ask_question(data):
        question = data.get('question')
        # Mock response using faker
        answer = fake.sentence()
        return {'question': question, 'answer': answer}