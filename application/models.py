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


exam_question = db.Table('exam_question',
                         db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"),
                                   primary_key=True),
                         db.Column('exam_id', db.Integer, db.ForeignKey('exam.id', ondelete="CASCADE"),
                                   primary_key=True)
                         )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(200), nullable=False)
    answers = db.relationship('Answer', backref='question', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<Question {}>'.format(self.question_title)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_title = db.Column(db.String(200), nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return '<Answer {}>'.format(self.answer_title)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    finished = db.Column(db.Boolean, default=False)
    points = db.Column(db.Numeric(precision=8, scale=2), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    question = db.relationship('Question', secondary=exam_question, lazy=True)

    def __repr__(self):
        return '<Exam {}>'.format(self.exam_title)
