import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, flash, redirect, url_for
from src.models.avaliacao import db, Avaliacao, Contato
from src.routes.avaliacao import avaliacao_bp
from src.routes.contato import contato_bp

# Criar aplicação Flask
app = Flask(__name__)

# Configuração do aplicativo
app.config['SECRET_KEY'] = 'coco_bambu_alphaville_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://coco_avaliacoes_user:wzjNTt8BRAlsAIV2YF0DKRyhfgIDYjEZ@dpg-d0mj8au3jp1c738d8rtg-a/coco_avaliacoes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)

# Registrar blueprints
app.register_blueprint(avaliacao_bp, url_prefix='')
app.register_blueprint(contato_bp, url_prefix='')

# Rota principal
@app.route('/')
def index():
    """Renderiza a página inicial"""
    avaliacoes_recentes = Avaliacao.query.filter_by(aprovada=True).order_by(Avaliacao.data_avaliacao.desc()).limit(3).all()
    avaliacoes_dict = [avaliacao.to_dict() for avaliacao in avaliacoes_recentes]
    return render_template('index.html', avaliacoes=avaliacoes_dict)

# Manipulador de erro 404
@app.errorhandler(404)
def page_not_found(e):
    """Renderiza página de erro 404 personalizada"""
    return render_template('404.html'), 404

# Manipulador de erro 500
@app.errorhandler(500)
def internal_server_error(e):
    """Renderiza página de erro 500 personalizada"""
    return render_template('500.html'), 500

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

    # Verificar se já existem avaliações no banco de dados
    if Avaliacao.query.count() == 0:
        avaliacao1 = Avaliacao(
            nome="Maria Silva",
            email="maria@exemplo.com",
            telefone="11999999999",
            qualidade=5,
            variedade=5,
            apresentacao=5,
            reposicao=4,
            atendimento=5,
            comentario="O buffet do Coco Bambu Alphaville superou todas as minhas expectativas!",
            pratos_favoritos="Camarões Grelhados, Moqueca de Peixe",
            frequencia="mensalmente",
            permissao_contato=True
        )
        avaliacao1.aprovada = True

        avaliacao2 = Avaliacao(
            nome="João Santos",
            email="joao@exemplo.com",
            telefone="11888888888",
            qualidade=4,
            variedade=5,
            apresentacao=4,
            reposicao=3,
            atendimento=5,
            comentario="Excelente variedade de frutos do mar.",
            pratos_favoritos="Paella de Frutos do Mar, Moqueca de Peixe",
            frequencia="raramente",
            permissao_contato=False
        )
        avaliacao2.aprovada = True

        avaliacao3 = Avaliacao(
            nome="Ana Oliveira",
            email="ana@exemplo.com",
            telefone="11777777777",
            qualidade=5,
            variedade=4,
            apresentacao=5,
            reposicao=5,
            atendimento=5,
            comentario="Frequento o Coco Bambu há anos. Qualidade incrível!",
            pratos_favoritos="Salmão ao Molho de Maracujá, Lagosta Grelhada",
            frequencia="semanalmente",
            permissao_contato=True
        )
        avaliacao3.aprovada = True

        db.session.add_all([avaliacao1, avaliacao2, avaliacao3])
        db.session.commit()

# Executar aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)