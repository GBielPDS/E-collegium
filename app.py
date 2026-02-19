from flask import Flask, request, jsonify # Importa o Flask para criar a API, request para pegar dados enviados e jsonify para retornar respostas em JSON
from flask_cors import CORS # Importa CORS para permitir requisições de outros domínios (ex.: frontend React)
from sqlalchemy import create_engine # Importa função para criar o engine do banco
from sqlalchemy.orm import sessionmaker # Importa sessionmaker para criar sessões de interação com o banco
from models import Base, Usuario # Importa a Base e o modelo Usuario definidos no arquivo models.py

app = Flask(__name__) # Cria a aplicação Flask
CORS(app) # Ativa o CORS na aplicação (permite conexões externas)
engine = create_engine("sqlite:///database.db") # Cria o engine apontando para um banco SQLite chamado database.db
Base.metadata.create_all(engine) # Cria todas as tabelas definidas em Base (se não existirem)
Session = sessionmaker(bind=engine) # Cria uma classe Session para abrir sessões com o banco

@app.route("/usuarios", methods=["POST"]) # Rota para criar um novo usuário (método POST)
def add_usuario():
 s = Session() # Abre uma sessão com o banco
 data = request.json # Pega o JSON enviado no corpo da requisição
 u = Usuario(nome=data["nome"], email=data["email"]) # Cria um objeto Usuario com os dados recebidos
 s.add(u) # Adiciona o usuário à sessão
 s.commit() # Confirma e grava no banco
 return jsonify({"message": "Usuário criado!"}) # Retorna uma resposta JSON