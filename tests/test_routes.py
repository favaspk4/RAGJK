import unittest
from flask import Flask, json
from flask_jwt_extended import create_access_token, JWTManager
from app import create_app
from app.models import User, Document, db

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.client = self.app.test_client()
        self.jwt = JWTManager(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.test_user = User(username='testuser', password='testpass', role='viewer')
        db.session.add(self.test_user)
        db.session.commit()

        self.access_token = create_access_token(identity={'id': self.test_user.id, 'username': self.test_user.username})

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        data = {'username': 'newuser', 'password': 'newpass', 'role': 'viewer'}
        response = self.client.post('/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_logout(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.post('/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_upload_document(self):
        data = {'filename': 'testfile.txt', 'file_url': 'http://example.com/testfile.txt'}
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.post('/upload', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_get_document(self):
        data = {'filename': 'testfile.txt', 'file_url': 'http://example.com/testfile.txt'}
        headers = {'Authorization': f'Bearer {self.access_token}'}
        upload_response = self.client.post('/upload', data=json.dumps(data), headers=headers, content_type='application/json')
        document_id = upload_response.json.get('document_id')

        # Now, retrieve the document
        response = self.client.get(f'/document/{document_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('filename', response.json)

if __name__ == '__main__':
    unittest.main()