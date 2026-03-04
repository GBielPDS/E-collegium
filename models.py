from sqlalchemy import Column, Integer, Float,String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    
    turma = relationship("Turma", back_populates="professor")

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey("usuarios.id"))
    nome = Column(String)
    escola = Column(String)
    nota_aprovacao = Column(Float)
    nota_recuperacao = Column(Float)
    nota_reprovacao = Column(Float)

    professor = relationship("Usuario", back_populates="turma")
    aluno = relationship("Aluno", back_populates="turma")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    nome = Column(String)
    nota1 = Column(Float)
    nota2 = Column(Float)
    nota3 = Column(Float)
    nota4 = Column(Float)
    nota_final = Column(Float)

    turma = relationship("Turma", back_populates="aluno")
