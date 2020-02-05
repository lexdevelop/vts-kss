import unittest
from . import db
from application.models import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_adding_new_user(self):
        user = User(username='test_username', email='test@test.com', first_name='test_fist', last_name='test_last')
        user.set_password('test_passwd')
        db.session.add(user)
        db.session.commit()
        self.assertIsInstance(user, User)
        self.assertEqual(1, user.id)
        self.assertEqual('test_username', user.username)
        self.assertEqual('test@test.com', user.email)
        self.assertEqual('test_fist', user.first_name)
        self.assertEqual('test_last', user.last_name)
        self.assertEqual(user.check_password('test_passwd'), True)
        self.assertEqual(user.check_password('test_passwd_not_correct'), False)
        self.assertEqual(1, User.query.count())
