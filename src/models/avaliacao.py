from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)  # Novo campo
    qualidade = db.Column(db.Integer, nullable=False)
    variedade = db.Column(db.Integer, nullable=False)
    apresentacao = db.Column(db.Integer, nullable=False)
    reposicao = db.Column(db.Integer, nullable=True)
    atendimento = db.Column(db.Integer, nullable=True)
    comentario = db.Column(db.Text, nullable=True)
    pratos_favoritos = db.Column(db.Text, nullable=True)
    sugestao_pratos = db.Column(db.Text, nullable=True)
    frequencia = db.Column(db.String(50), nullable=True)
    permissao_contato = db.Column(db.Boolean, default=False)
    aprovada = db.Column(db.Boolean, default=False)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def media_geral(self):
        notas = [self.qualidade, self.variedade, self.apresentacao]
        if self.reposicao:
            notas.append(self.reposicao)
        if self.atendimento:
            notas.append(self.atendimento)
        return round(sum(notas) / len(notas), 1)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'qualidade': self.qualidade,
            'variedade': self.variedade,
            'apresentacao': self.apresentacao,
            'reposicao': self.reposicao,
            'atendimento': self.atendimento,
            'comentario': self.comentario,
            'pratos_favoritos': self.pratos_favoritos,
            'sugestao_pratos': self.sugestao_pratos,
            'frequencia': self.frequencia,
            'permissao_contato': self.permissao_contato,
            'aprovada': self.aprovada,
            'data_avaliacao': self.data_avaliacao.strftime('%d/%m/%Y'),
            'media_geral': self.media_geral
        }

class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    assunto = db.Column(db.String(120), nullable=True)
    mensagem = db.Column(db.Text, nullable=False)
    newsletter = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)