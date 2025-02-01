import unittest
from flask import Flask
from app.utils import init_db, init_auth

class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)

        init_db(cls.app)
        init_auth(cls.app)

        cls.client = cls.app.test_client()

    def test_init_db(self):
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'],
                         'postgresql://postgres:1234@localhost/flask_rag_db')
        self.assertFalse(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])  # Should be False

    def test_init_auth(self):
        self.assertEqual(self.app.config['JWT_SECRET_KEY'], 'your-secret-key')
        self.assertEqual(self.app.config["JWT_ACCESS_TOKEN_EXPIRES"].minutes, 10)

    def test_jwt_client(self):
        response = self.client.get('/protected', headers={'Authorization': 'Bearer some_token'})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
