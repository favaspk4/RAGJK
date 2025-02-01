import unittest
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.datastructures import FileStorage
from app.services import AuthService, DocumentService, QAService
from app.models import User, Document, db

class TestServices(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.app.config['UPLOAD_FOLDER'] = 'test_uploads'
        self.jwt = JWTManager(self.app)

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        for filename in os.listdir(self.app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.app.config['UPLOAD_FOLDER'])

    def test_auth_service_register(self):
        data = {'username': 'testuser', 'password': 'testpass', 'role': 'user'}
        response, status_code = AuthService.register(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'User Registered Successfully')

        response, status_code = AuthService.register(data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'username already exists')

    def test_auth_service_login(self):
        user = User(username='testuser', role='user')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()

        data = {'username': 'testuser', 'password': 'testpass'}
        response, status_code = AuthService.login(data)
        self.assertEqual(status_code, 200)
        self.assertIn('access_token', response)

        data = {'username': 'testuser', 'password': 'wrongpass'}
        response, status_code = AuthService.login(data)
        self.assertEqual(status_code, 401)
        self.assertEqual(response['message'], 'Invalid Credentials')

    def test_auth_service_logout(self):
        response, status_code = AuthService.logout()
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'User logged out successfully')

    def test_document_service_upload_document(self):
        with self.app.app_context():
            file = FileStorage(filename='testfile.txt', stream=open('testfile.txt', 'rb'))

            response, status_code = DocumentService.upload_document(file)
            self.assertEqual(status_code, 201)
            self.assertEqual(response['message'], 'File uploaded successfully')
            self.assertIsNotNone(response['document_id'])

            # Verify the document was saved in the database
            document = Document.query.get(response['document_id'])
            self.assertIsNotNone(document)
            self.assertEqual(document.filename, 'testfile.txt')

    def test_document_service_get_document(self):
        with self.app.app_context():
            document = Document(filename='testfile.txt', file_url='http://example.com/testfile.txt')
            db.session.add(document)
            db.session.commit()

            response, status_code = DocumentService.get_document(document.id)
            self.assertEqual(status_code, 200)
            self.assertEqual(response['filename'], 'testfile.txt')
            self.assertEqual(response['file_url'], 'http://example.com/testfile.txt')

            # Test retrieving a non-existent document
            response, status_code = DocumentService.get_document(999)
            self.assertEqual(status_code, 404)
            self.assertEqual(response['error'], 'Document not found')

    def test_qa_service_ask_question(self):
        data = {'question': 'What is the capital of France?'}
        response = QAService.ask_question(data)
        self.assertIn('question', response)
        self.assertIn('answer', response)
        self.assertEqual(response['question'], 'What is the capital of France?')

if __name__ == '__main__':
    unittest.main()