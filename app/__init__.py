from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from flasgger import Swagger

# Instâncias dos pacotes
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    # Criação da instância do Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # Todos os endpoints
                "model_filter": lambda tag: True,  # Todos os modelos
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "info": {
            "title": "API Carford",
            "description": "Documentação da API Carford",
            "version": "1.0.0"
        }
    }

    # Inicializando o Swagger com configuração customizada
    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    # Inicialização do SQLAlchemy e Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Inicializando JWT
    jwt.init_app(app)

    # Registrando Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
