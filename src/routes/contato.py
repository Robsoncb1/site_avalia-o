from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.avaliacao import db, Contato

# Criar blueprint para rotas de contato
contato_bp = Blueprint('contato', __name__)

@contato_bp.route('/contato')
def contato():
    """Renderiza a página de contato"""
    return render_template('contato.html')

@contato_bp.route('/submit_contato', methods=['POST'])
def submit_contato():
    """Processa o envio do formulário de contato"""
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            nome = request.form.get('name')
            email = request.form.get('email')
            telefone = request.form.get('phone')
            assunto = request.form.get('subject')
            mensagem = request.form.get('message')
            
            # Verificar se deseja receber newsletter
            newsletter = True if request.form.get('newsletter') else False
            
            # Criar nova mensagem de contato
            novo_contato = Contato(
                nome=nome,
                email=email,
                telefone=telefone,
                assunto=assunto,
                mensagem=mensagem,
                newsletter=newsletter
            )
            
            # Salvar no banco de dados
            db.session.add(novo_contato)
            db.session.commit()
            
            # Redirecionar com mensagem de sucesso
            flash('Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            # Em caso de erro, fazer rollback e mostrar mensagem
            db.session.rollback()
            flash(f'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente.', 'error')
            print(f"Erro ao processar contato: {str(e)}")
            return redirect(url_for('contato.contato'))

@contato_bp.route('/sobre')
def sobre():
    """Renderiza a página sobre o restaurante"""
    return render_template('sobre.html')

@contato_bp.route('/menu')
def menu():
    """Renderiza a página de menu do buffet"""
    return render_template('menu.html')
