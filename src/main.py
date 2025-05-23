import sys
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from src.models.avaliacao import db, Avaliacao

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'coco_bambu_alphaville_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://coco_avaliacoes_user:wzjNTt8BRAlsAIV2YF0DKRyhfgIDYjEZ@dpg-d0mj8au3jp1c738d8rtg-a/coco_avaliacoes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def avaliar():
    sucesso = session.pop('sucesso', False)
    return render_template('avaliar.html', sucesso=sucesso)

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        # Verificação obrigatória dos campos de nota
        obrigatorios = ['qualidade', 'variedade', 'apresentacao', 'reposicao', 'atendimento']
        for campo in obrigatorios:
            if not request.form.get(campo):
                flash(f'O campo {campo} é obrigatório.', 'danger')
                return redirect(url_for('avaliar'))

        nova = Avaliacao(
            nome=request.form.get('nome'),
            qualidade=int(request.form['qualidade']),
            variedade=int(request.form['variedade']),
            apresentacao=int(request.form['apresentacao']),
            reposicao=int(request.form['reposicao']),
            atendimento=int(request.form['atendimento']),
            comentario=request.form.get('comentario'),
            pratos_favoritos=request.form.get('pratos_favoritos'),
            sugestao_pratos=request.form.get('sugestao_pratos'),
            frequencia=request.form.get('frequencia'),
            permissao_contato=request.form.get('permissao_contato') == 'sim',
            telefone=request.form.get('telefone') or None,
            data_avaliacao=datetime.now(),
            aprovada=True
        )
        db.session.add(nova)
        db.session.commit()
        session['sucesso'] = True
    except Exception as e:
        print("Erro ao salvar avaliação:", e)
        session['sucesso'] = False

    return redirect(url_for('avaliar'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'suasenha123':
            session['admin'] = True
            return redirect('/avaliacoes')
    return render_template('admin_login.html')

@app.route('/avaliacoes')
def admin_avaliacoes():
    if not session.get('admin'):
        return redirect('/admin')
    avaliacoes = Avaliacao.query.order_by(Avaliacao.data_avaliacao.desc()).all()
    return render_template('admin_avaliacoes.html', avaliacoes=avaliacoes)

with app.app_context():
    db.create_all()
    if Avaliacao.query.count() == 0:
        exemplo = Avaliacao(
            nome="Maria Silva",
            qualidade=5,
            variedade=5,
            apresentacao=5,
            reposicao=4,
            atendimento=5,
            comentario="Excelente buffet!",
            pratos_favoritos="Camarões Grelhados",
            sugestao_pratos="Bobó de Camarão",
            frequencia="frequentemente",
            permissao_contato=True,
            telefone="11999999999",
            aprovada=True,
            data_avaliacao=datetime.now()
        )
        db.session.add(exemplo)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)