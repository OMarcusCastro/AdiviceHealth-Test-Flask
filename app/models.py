from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)
    owner = db.relationship('Owner', uselist=False, back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sale_opportunity = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='owner')

    cars = db.relationship('Car', backref='owner',
                           lazy=True, cascade="all, delete-orphan")


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum('yellow', 'blue', 'gray',
                      name='color_enum'), nullable=False)
    model = db.Column(db.Enum('hatch', 'sedan', 'convertible',
                      name='model_enum'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'owners.id'), nullable=False)
