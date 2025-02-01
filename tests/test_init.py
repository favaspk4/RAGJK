import unittest
from flask import Flask
from app import create_app

class TestAppInitialization(unittest.TestCase):

    def test_create_app(self):
        app = create_app()
        self.assertIsInstance(app, Flask)

    def test_app_configuration(self):
        app = create_app()
        self.assertTrue(app.config['DEBUG'] is not None)

    def test_database_initialization(self):
        app = create_app()
        with app.app_context():
            self.assertTrue(hasattr(app, 'extensions'))
            self.assertIn('sqlalchemy', app.extensions)

    def test_auth_initialization(self):
        app = create_app()
        with app.app_context():
            self.assertTrue(hasattr(app, 'extensions'))
            self.assertIn('auth', app.extensions)

    def test_routes_initialization(self):
        app = create_app()
        self.assertIn('/some-route', [str(p) for p in app.url_map.iter_rules()])

if __name__ == '__main__':
    unittest.main()