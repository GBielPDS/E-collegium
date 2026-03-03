from flask import Flask, request, jsonify # Importa o Flask para criar a API, request para pegar dados enviados e jsonify para retornar respostas em JSON
from flask_cors import CORS # Importa CORS para permitir requisições de outros domínios (ex.: frontend React)
from sqlalchemy import create_engine # Importa função para criar o engine do banco
from sqlalchemy.orm import sessionmaker # Importa sessionmaker para criar sessões de interação com o banco
from models import Base, Usuario, Turma, Aluno # Importa a Base e o modelo Usuario definidos no arquivo models.py

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

@app.route("/usuarios", methods=["GET"]) # Rota para listar todos os usuários (método GET)
def get_usuarios():
 s = Session() # Abre uma sessão com o banco
 usuarios = s.query(Usuario).all() # Consulta todos os usuários
 # Retorna uma lista de dicionários contendo os campos dos usuários
 return jsonify([
 {"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios
 ])

@app.route("/usuarios/<int:id>", methods=["GET"])
def get_unique_usuario(id):
    s = Session()
    usuario = s.query(Usuario).get(id)
    return jsonify([
        {"id": usuario.id, "nome": usuario.nome, "email": usuario.email}
    ])

@app.route("/turmas", methods=["POST"])
def add_turma():
    s = Session() 
    data = request.json 
    turma = Turma(
      professor_id=data["professor_id"],
      nome=data["nome"], escola=data["escola"], 
      nota_aprovacao=data["nota_aprovacao"], 
      nota_recuperacao=data["nota_recuperacao"], 
      nota_reprovacao=data["nota_reprovacao"]) 
    s.add(turma) 
    s.commit() 
    return jsonify({"message": "Turma criada!"})

if __name__ == "__main__":
 app.run(debug=True) # debug=True reinicia o servidor automaticamente