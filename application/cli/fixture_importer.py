from application import db
from application.models import User


def import_fixture(fixture):
    fixture_model = fixture['model']
    if fixture_model == 'User':
        import_user_fixture(fixture)


def import_user_fixture(fixture):
    for user in fixture['data']:
        user_model = User(username=user['username'], email=user['email'], first_name=user['first_name'],
                          last_name=user['last_name'])
        user_model.set_password(user['password'])
        db.session.add(user_model)

    db.session.commit()
