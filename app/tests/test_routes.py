import pytest
from app import create_app, db
from app.models import User, Owner, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,

        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test_jwt_secret_key'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def access_token(app):
    with app.app_context():
        user = User(username='testuser',
                    password_hash=generate_password_hash('testpass'))
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        return token


def test_register_user_and_owner(client):
    # Criar um usuário e garantir que um Owner seja associado
    response = client.post('/register', json={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 201

    # Verificar se o Owner foi criado
    user = User.query.filter_by(username='newuser').first()
    assert user.owner is not None


def test_login(client):

    client.post('/register', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })

    response = client.post('/login', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()


def test_owner_creation_with_user(client):

    response = client.post('/register', json={
        'username': 'owneruser',
        'password': 'password123'
    })
    assert response.status_code == 201

    user = User.query.filter_by(username='owneruser').first()
    assert user is not None

    owner = Owner.query.filter_by(user_id=user.id).first()
    assert owner is not None
    assert owner.name == 'owneruser'


def test_add_car(client, access_token):

    client.post('/register', json={
        'username': 'user_with_car',
        'password': 'password123'
    })
    user = User.query.filter_by(username='user_with_car').first()

    response = client.post('/car', json={
        'color': 'blue',
        'model': 'hatch',
        'owner_id': user.owner.id
    }, headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Car added successfully'
