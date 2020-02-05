import unittest
from . import app


class TestConfig(unittest.TestCase):
    def test_config(self):
        self.assertEqual(app.config['DEBUG'], True)
        self.assertEqual(app.config['TESTING'], True)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')
