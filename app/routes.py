from flask import Blueprint, request, jsonify
from . import db
from .models import User, Owner, Car
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)


@main.route('/register', methods=['POST'])
def register():
    # flasgger
    """
    Register a new user and owner
    ---
    tags:
        - users
    parameters: 
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        201:
            description: User and Owner registered successfully
        400:
            description: User already exists
    """

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verifica se o usuário já existe
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    # Cria o usuário
    new_user = User(username=username)
    new_user.set_password(password)

    # Cria o owner associado ao usuário
    # O nome do proprietário será o nome de usuário, mas pode ser modificado
    new_owner = Owner(name=username, user=new_user)

    # Adiciona ambos ao banco de dados
    db.session.add(new_user)
    db.session.add(new_owner)
    db.session.commit()

    return jsonify({'message': 'User and Owner registered successfully'}), 201


@main.route('/login', methods=['POST'])
def login():

    # swagger
    """
    Login
    ---
    tags:

        - users
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        200:
            description: Access token generated successfully
        401:
            description: Invalid credentials
    """

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


# @main.route('/owner', methods=['POST'])
# @jwt_required()
# def add_owner():
#     data = request.get_json()
#     new_owner = Owner(name=data['name'], sale_opportunity=True)
#     db.session.add(new_owner)
#     db.session.commit()
#     return jsonify({'message': 'Owner added successfully'}), 201


@main.route('/car', methods=['POST'])
@jwt_required()
def add_car():

    # swagger
    """

    Add a new car
    ---
    tags:
        - cars
    parameters: 
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                color:
                    type: string
                model:
                    type: string
                owner_id:
                    type: integer
    responses:
        201:
            description: Car added successfully
        400:
            description: Invalid color or model
        404:
            description: Owner not found
    """

    data = request.get_json()
    owner = db.session.get(Owner, data['owner_id'])

    if not owner:
        return jsonify({'message': 'Owner not found'}), 404
    if len(owner.cars) >= 3:
        return jsonify({'message': 'Owner already has 3 cars'}), 400

    color = data.get('color')
    model = data.get('model')

    if color not in ['yellow', 'blue', 'gray']:
        return jsonify({'message': 'Invalid color'}), 400
    if model not in ['hatch', 'sedan', 'convertible']:
        return jsonify({'message': 'Invalid model'}), 400

    new_car = Car(color=color, model=model, owner_id=data['owner_id'])
    db.session.add(new_car)
    db.session.commit()

    return jsonify({'message': 'Car added successfully'}), 201


@main.route('/owners', methods=['GET'])
@jwt_required()
def get_owners():
    """
    Get all owners
    ---
    tags:
        - owners
    responses:
        200:
            description: List of all owners

    """
    owners = Owner.query.all()
    owners_data = []
    for owner in owners:
        owners_data.append({
            'id': owner.id,
            'name': owner.name,
            'sale_opportunity': owner.sale_opportunity,
            'cars': [{'id': car.id, 'color': car.color, 'model': car.model} for car in owner.cars]
        })
    return jsonify(owners_data), 200


@main.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    cars = Car.query.all()
    cars_data = []
    for car in cars:
        cars_data.append({
            'id': car.id,
            'color': car.color,
            'model': car.model,
            'owner_id': car.owner_id
        })
    return jsonify(cars_data), 200
