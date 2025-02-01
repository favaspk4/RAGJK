import unittest
from datetime import datetime
from app import create_app
from app.models import User, Document, Embedding, db

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser', password='testpass', role='viewer')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.role, 'viewer')

    def test_document_creation(self):
        document = Document(filename='testfile.txt', file_url='http://example.com/testfile.txt')
        db.session.add(document)
        db.session.commit()

        retrieved_document = Document.query.filter_by(filename='testfile.txt').first()
        self.assertIsNotNone(retrieved_document)
        self.assertEqual(retrieved_document.file_url, 'http://example.com/testfile.txt')
        self.assertIsInstance(retrieved_document.uploaded_at, datetime)

    def test_embedding_creation(self):
        document = Document(filename='testfile.txt', file_url='http://example.com/testfile.txt')
        db.session.add(document)
        db.session.commit()

        embedding = Embedding(document_id=document.id, embedding='{"key": "value"}')
        db.session.add(embedding)
        db.session.commit()

        retrieved_embedding = Embedding.query.filter_by(document_id=document.id).first()
        self.assertIsNotNone(retrieved_embedding)
        self.assertEqual(retrieved_embedding.embedding, '{"key": "value"}')

    def test_user_unique_username(self):
        user1 = User(username='testuser', password='testpass', role='viewer')
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='testuser', password='anotherpass', role='editor')
        db.session.add(user2)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_document_embedding_relationship(self):
        document = Document(filename='testfile.txt', file_url='http://example.com/testfile.txt')
        db.session.add(document)
        db.session.commit()

        embedding = Embedding(document_id=document.id, embedding='{"key": "value"}')
        db.session.add(embedding)
        db.session.commit()

        retrieved_document = Document.query.get(document.id)
        self.assertEqual(len(retrieved_document.embeddings), 1)
        self.assertEqual(retrieved_document.embeddings[0].embedding, '{"key": "value"}')

if __name__ == '__main__':
    unittest.main()