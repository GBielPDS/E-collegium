from flask import Flask, request, jsonify # Importa o Flask para criar a API, request para pegar dados enviados e jsonify para retornar respostas em JSON
from flask_cors import CORS # Importa CORS para permitir requisições de outros domínios (ex.: frontend React)
from sqlalchemy import create_engine # Importa função para criar o engine do banco
from sqlalchemy.orm import sessionmaker # Importa sessionmaker para criar sessões de interação com o banco
from models import Base, Usuario, Turma, Aluno # Importa a Base e o modelo Usuario definidos no arquivo models.py
from sqlalchemy.exc import IntegrityError


app = Flask(__name__) # Cria a aplicação Flask
CORS(app) # Ativa o CORS na aplicação (permite conexões externas)
engine = create_engine("sqlite:///database.db") # Cria o engine apontando para um banco SQLite chamado database.db
Base.metadata.create_all(engine) # Cria todas as tabelas definidas em Base (se não existirem)
Session = sessionmaker(bind=engine) # Cria uma classe Session para abrir sessões com o banco

@app.route("/usuarios", methods=["POST"]) # Rota para criar um novo usuário (método POST)
def add_usuario():
 s = Session() # Abre uma sessão com o banco
 data = request.json # Pega o JSON enviado no corpo da requisição
 u = Usuario(nome=data["nome"], email=data["email"], senha=data["senha"]) # Cria um objeto Usuario com os dados recebidos
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

@app.route("/usuarios/<int:id>", methods=["PUT"])
def update_usuario(id):
    s = Session()
    usuario = s.get(Usuario, id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()

    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)
    usuario.senha = data.get("senha", usuario.senha)

    s.commit()

    return jsonify({"message": "Usuário atualizado!"})

@app.route("/usuarios/<int:id>/turmas", methods=["GET"])
def get_all_turmas_professor(id):
    s = Session()
    turmas = s.query(Turma).filter_by(professor_id=id).all()

    return jsonify([
        {
            "id": t.id,
            "professor_id": t.professor_id,
            "nome": t.nome,
            "escola": t.escola,
            "nota_aprovacao": t.nota_aprovacao,
            "nota_recuperacao": t.nota_recuperacao,
            "nota_reprovacao": t.nota_reprovacao
        }
        for t in turmas
    ])

#########   Turma   #########



@app.route("/register", methods=["POST"])
def register():
    s = Session()
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"error": "Preencha todos os campos"}), 400

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha 
    )

    try:
        s.add(novo_usuario)
        s.commit()
    except IntegrityError:
        s.rollback()
        return jsonify({"error": "Email já cadastrado"}), 400

    return jsonify({
        "message": "Usuário cadastrado com sucesso!",
        "id": novo_usuario.id,
        "nome": novo_usuario.nome
    }), 201

@app.route("/login", methods=["POST"])
def login():
    s = Session()
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Email e senha obrigatórios"}), 400

    usuario = s.query(Usuario).filter_by(email=email).first()

    if not usuario or usuario.senha != senha:
        return jsonify({"error": "Credenciais inválidas"}), 401

    return jsonify({
        "message": "Login realizado com sucesso",
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    })

#########   Turma   #########

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

@app.route("/turmas", methods=["GET"])
def get_turmas():
    s = Session()
    turmas = s.query(Turma).all()

    return jsonify([
        {
            "id": t.id,
            "professor_id": t.professor_id,
            "nome": t.nome,
            "escola": t.escola,
            "nota_aprovacao": t.nota_aprovacao,
            "nota_recuperacao": t.nota_recuperacao,
            "nota_reprovacao": t.nota_reprovacao
        }
        for t in turmas
    ])

@app.route("/turmas/<int:id>", methods=["PUT"])
def update_turma(id):
    s = Session()
    turma = s.get(Turma, id)

    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    data = request.get_json()

    turma.nome = data.get("nome", turma.nome)
    turma.escola = data.get("escola", turma.escola)
    turma.nota_aprovacao = data.get("nota_aprovacao", turma.nota_aprovacao)
    turma.nota_recuperacao = data.get("nota_recuperacao", turma.nota_recuperacao)
    turma.nota_reprovacao = data.get("nota_reprovacao", turma.nota_reprovacao)

    s.commit()

    return jsonify({"message": "Turma atualizada!"})

@app.route("/turmas/<int:id>", methods=["DELETE"])
def delete_turma(id):
    s = Session()
    turma = s.get(Turma, id)

    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404
    
    s.query(Aluno).filter_by(turma_id=id).delete()
    
    s.delete(turma)
    s.commit()

    return jsonify({"message": "Turma excluída"})

@app.route("/turmas/<int:turma_id>/alunos", methods=["GET"])
def get_all_aluno_turma(turma_id):
    s = Session()
    alunos = s.query(Aluno).filter_by(turma_id=turma_id).all()

    if not alunos:
        return jsonify({"error": "Nenhum aluno encontrado"}), 404

    return jsonify([
        {
            "id": a.id,
            "turma_id": a.turma_id,
            "nome": a.nome,
            "nota1": a.nota1,
            "nota2": a.nota2,
            "nota3": a.nota3,
            "nota4": a.nota4,
            "nota_final": a.nota_final
        }
        for a in alunos
    ])



#########   Aluno   #########

@app.route("/alunos", methods=["POST"])
def add_aluno():
    s = Session()
    data = request.get_json()
    aluno = Aluno(
        turma_id=data["turma_id"],
        nome=data["nome"],
        nota1=data["nota1"],
        nota2=data["nota2"],
        nota3=data["nota3"],
        nota4=data["nota4"],
        nota_final=data["nota_final"]
    )

    s.add(aluno)
    s.commit()

    return jsonify({"message": "Aluno criado!"}), 201

@app.route("/alunos", methods=["GET"])
def get_alunos():
    s = Session()
    alunos = s.query(Aluno).all()

    return jsonify([
        {
            "id": a.id,
            "turma_id": a.turma_id,
            "nome": a.nome,
            "nota1": a.nota1,
            "nota2": a.nota2,
            "nota3": a.nota3,
            "nota4": a.nota4,
            "nota_final": a.nota_final
        }
        for a in alunos
    ])

@app.route("/alunos/<int:id>", methods=["GET"])
def get_unique_aluno(id):
    s = Session()
    aluno = s.get(Aluno, id)

    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    return jsonify({
        "id": aluno.id,
        "turma_id": aluno.turma_id,
        "nome": aluno.nome,
        "nota1": aluno.nota1,
        "nota2": aluno.nota2,
        "nota3": aluno.nota3,
        "nota4": aluno.nota4,
        "nota_final": aluno.nota_final
    })


@app.route("/alunos/<int:id>", methods=["PUT"])
def update_aluno(id):
    s = Session()
    aluno = s.get(Aluno, id)

    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    data = request.get_json()

    aluno.nome = data.get("nome", aluno.nome)
    aluno.nota1 = data.get("nota1", aluno.nota1)
    aluno.nota2 = data.get("nota2", aluno.nota2)
    aluno.nota3 = data.get("nota3", aluno.nota3)
    aluno.nota4 = data.get("nota4", aluno.nota4)

    aluno.nota_final = data.get("nota_final", aluno.nota_final)

    s.commit()

    return jsonify({"message": "Aluno atualizado!"})

@app.route("/alunos/<int:id>", methods=["DELETE"])
def delete_aluno(id):
    s = Session()
    aluno = s.get(Aluno, id)

    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    s.delete(aluno)
    s.commit()

    return jsonify({"message": "Aluno excluído"})


if __name__ == "__main__":
 app.run(debug=True) # debug=True reinicia o servidor automaticamente