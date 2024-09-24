# AdiviceHealth Flask Application

Este é um projeto Flask que utiliza SQLAlchemy, PostgreSQL e Docker para gerenciar uma aplicação simples de registro de usuários, criação de proprietários e gerenciamento de carros.

## Features

- Registro de usuários
- Relacionamento entre `User` e `Owner` (todo `User` é um `Owner`)
- Adição de carros associados aos proprietários
- Segurança nas rotas com JWT
- Migrações de banco de dados com Flask-Migrate
- Testes com Pytest

## Endpoints
-[Swagger](http://localhost:8000/apidocs/)

## Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+
- [PostgreSQL](https://www.postgresql.org/)

## Instalação

1. Clone o repositório:

```bash
   
   git clone https://github.com/seu-usuario/adivicehealth-flask.git
   cd adivicehealth-flask
```

## Crie o arquivo .env na raiz do projeto com suas variáveis de ambiente:


Construa e execute os contêineres Docker:

```bash
Copy code
docker-compose up --build
```

Instale as dependências dentro do contêiner Docker:

```bash
docker-compose run web pip install -r requirements.txt
```

Crie o banco de dados e aplique as migrações:

```bash
docker-compose run web flask db init
docker-compose run web flask db migrate -m "Initial migration"
docker-compose run web flask db upgrade
```



A aplicação estará rodando em http://localhost:8000.

Exemplos de Uso
Registro de Usuário
Para registrar um novo usuário que automaticamente se tornará um proprietário (Owner):

Exemplo de Requisição

POST /register

```json
{
    "username": "newuser",
    "password": "newpassword"
}   
```

Resposta de Sucesso

```json

{
    "message": "User registered successfully"
}
```

Login de Usuário
Logar com um usuário registrado para obter um token JWT:

Exemplo de Requisição

```bash

POST /login
{
    "username": "newuser",
    "password": "newpassword"
}
```

Resposta de Sucesso

```json

{
    "access_token": "seu_token_jwt_aqui"
}

```

Adicionar Carro
Adicionar um carro a um proprietário existente (que é um usuário registrado):

Exemplo de Requisição

```bash
POST /add_car
{
    "owner_id": 1,
    "color": "yellow",
    "model": "sedan"
}
```

Resposta de Sucesso

```json

{
    "message": "Car added successfully"
}
```

Visualizar Perfil de Usuário (Protegido)
Este endpoint permite ao usuário autenticado visualizar seu perfil, incluindo o ID do proprietário associado. Requer um token JWT.

Exemplo de Requisição
bash
Copy code
GET /profile
Authorization: Bearer seu_token_jwt_aqui
Resposta de Sucesso

```json

{
    "username": "newuser",
    "owner_id": 1
}
```

Rodando os Testes
Para rodar os testes utilizando Pytest, basta executar o comando a seguir:

bash
Copy code
docker-compose run web pytest
Os testes cobrem cenários como:

Registro de novos usuários
Login de usuários
Adicionar carros a proprietários
Verificar a criação de proprietários associados
Exemplo de Saída de Testes
```bash

================================================= test session starts ==================================================
platform linux -- Python 3.11.10, pytest-8.3.3, pluggy-1.5.0
rootdir: /app
plugins: flask-1.3.0
collected 4 items                                                                                                      

app/tests/test_routes.py ....                                                                                      [100%]

================================================= 4 passed in 0.45s ===================================================
Estrutura do Projeto
bash
Copy code
.
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── tests
│   │   └── test_routes.py
│   ├── config.py
├── migrations
│   └── ...
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
Tecnologias Utilizadas
Flask: Framework web minimalista
SQLAlchemy: ORM para interação com banco de dados
PostgreSQL: Banco de dados relacional
Flask-JWT-Extended: Implementação de JWT para autenticação
Flask-Migrate: Ferramenta para migrações de banco de dados
Pytest: Framework para testes
Docker: Para contêineres e gerenciamento de ambiente
Contribuição
Faça um fork do projeto
Crie uma nova branch (git checkout -b feature/nome-da-feature)
Faça commit de suas mudanças (git commit -am 'Add new feature')
Faça push para a branch (git push origin feature/nome-da-feature)
Abra um Pull Request
Licença
Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo LICENSE para mais detalhes.

lua
Copy code

Este `README.md` inclui instruções sobre como rodar o projeto, instalar dependências, utilizar os endpoints, e também como rodar os testes dentro do ambiente Docker. Certifique-se de substituir os placeholders, como `seu-usuario`, conforme necessário.

```



