import random
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from application import db, login_manager
from flask_login import UserMixin
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(200), nullable=False)
    answers = db.relationship('Answer', backref='question', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<Question {}>'.format(self.question_title)

    def count_records(self):
        return self.query.count()

    def random_questions(self):
        return random.choice(self.query.all())

    # This is not working with SQLite, it require additional math library installation
    def optimized_random(self, limit):
        return self.query.offset(
            func.floor(
                func.random() *
                db.session.query(func.count(self.id))
            )
        ).limit(limit).all()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_title = db.Column(db.String(200), nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return '<Answer {}>'.format(self.answer_title)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    result_payload = db.Column(db.PickleType)

    def __repr__(self):
        return '<Exam {}>'.format(self.exam_title)
