from application import db
from application.models import User, Question, Answer


def import_fixture(fixture):
    fixture_model = fixture['model']
    if fixture_model == 'User':
        import_user_fixture(fixture)
    if fixture_model == 'Question':
        import_question_fixture(fixture)


def import_user_fixture(fixture):
    for user in fixture['data']:
        user_model = User(username=user['username'], email=user['email'], first_name=user['first_name'],
                          last_name=user['last_name'])
        user_model.set_password(user['password'])
        db.session.add(user_model)

    db.session.commit()


def import_question_fixture(fixture):
    for question in fixture['data']:
        question_model = Question(question_title=question['question_title'])
        db.session.add(question_model)
        for answer in question['answers']:
            answer_model = Answer(answer_title=answer['answer_title'], correct=answer['correct'],
                                  question=question_model)
            db.session.add(answer_model)

    db.session.commit()
