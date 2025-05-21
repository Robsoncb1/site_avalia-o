from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from src.models.avaliacao import db, Avaliacao
from datetime import datetime, timedelta
from src.config_email import enviar_email_avaliacao

avaliacao_bp = Blueprint('avaliacao', __name__)

@avaliacao_bp.route('/avaliar')
def avaliar():
    return render_template('avaliar.html')

@avaliacao_bp.route('/submit_avaliacao', methods=['POST'])
def submit_avaliacao():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            qualidade = int(request.form.get('qualidade'))
            variedade = int(request.form.get('variedade'))
            apresentacao = int(request.form.get('apresentacao'))
            reposicao = int(request.form.get('reposicao')) if request.form.get('reposicao') else 0
            atendimento = int(request.form.get('atendimento')) if request.form.get('atendimento') else 0
            comentario = request.form.get('comentario')
            pratos_favoritos = request.form.get('pratos_favoritos')
            sugestao_pratos = request.form.get('sugestao_pratos')
            frequencia = request.form.get('frequencia')
            permissao_contato = request.form.get('permissao_contato') == 'sim'

            nova_avaliacao = Avaliacao(
                nome=nome,
                email=email,
                telefone=telefone,
                qualidade=qualidade,
                variedade=variedade,
                apresentacao=apresentacao,
                reposicao=reposicao,
                atendimento=atendimento,
                comentario=comentario,
                pratos_favoritos=pratos_favoritos,
                sugestao_pratos=sugestao_pratos,
                frequencia=frequencia,
                permissao_contato=permissao_contato
            )

            db.session.add(nova_avaliacao)
            db.session.commit()

            # Enviar e-mail para a diretoria
            enviar_email_avaliacao(nome, comentario, pratos_favoritos, sugestao_pratos, nova_avaliacao.media_geral)

            # Mostrar mensagem de sucesso
            return render_template('avaliar.html', sucesso=True)

        except Exception as e:
            db.session.rollback()
            flash('Ocorreu um erro ao processar sua avaliação. Por favor, tente novamente.', 'error')
            print(f"Erro ao processar avaliação: {str(e)}")
            return redirect(url_for('avaliacao.avaliar'))

@avaliacao_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'coco@2025':
            session['admin'] = True
            return redirect(url_for('avaliacao.admin_avaliacoes'))
        else:
            flash("Senha incorreta.", "error")
            return render_template('admin_login.html')
    return render_template('admin_login.html')

@avaliacao_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('avaliacao.avaliar'))

@avaliacao_bp.route('/admin/avaliacoes')
def admin_avaliacoes():
    if not session.get('admin'):
        flash("Acesso restrito. Faça login como administrador.", "error")
        return redirect(url_for('avaliacao.admin_login'))

    filtro_data = request.args.get('data', '')
    filtro_nota = request.args.get('nota', '')

    query = Avaliacao.query

    if filtro_data.isdigit():
        dias = int(filtro_data)
        data_limite = datetime.utcnow() - timedelta(days=dias)
        query = query.filter(Avaliacao.data_avaliacao >= data_limite)

    if filtro_nota.isdigit():
        nota = int(filtro_nota)
        if nota in range(1, 6):
            query = query.filter(
                (Avaliacao.qualidade >= nota) |
                (Avaliacao.variedade >= nota) |
                (Avaliacao.apresentacao >= nota) |
                (Avaliacao.reposicao >= nota) |
                (Avaliacao.atendimento >= nota)
            )

    avaliacoes = query.order_by(Avaliacao.data_avaliacao.desc()).all()
    return render_template('admin_avaliacoes.html', avaliacoes=avaliacoes, filtro_data=filtro_data, filtro_nota=filtro_nota)

@avaliacao_bp.route('/feedback')
def feedback():
    rating_filter = request.args.get('rating', '')
    date_filter = request.args.get('date', '')
    query = Avaliacao.query.filter_by(aprovada=True)

    if rating_filter:
        query = query.filter(Avaliacao.media_geral >= int(rating_filter))

    if date_filter:
        today = datetime.utcnow()
        if date_filter == 'week':
            date_limit = today - timedelta(days=7)
        elif date_filter == 'month':
            date_limit = today - timedelta(days=30)
        elif date_filter == 'year':
            date_limit = today - timedelta(days=365)
        query = query.filter(Avaliacao.data_avaliacao >= date_limit)

    avaliacoes = query.order_by(Avaliacao.data_avaliacao.desc()).all()
    avaliacoes_dict = [avaliacao.to_dict() for avaliacao in avaliacoes]
    return render_template('feedback.html', avaliacoes=avaliacoes_dict)

@avaliacao_bp.route('/api/avaliacoes')
def api_avaliacoes():
    rating_filter = request.args.get('rating', '')
    date_filter = request.args.get('date', '')
    query = Avaliacao.query.filter_by(aprovada=True)

    if rating_filter:
        query = query.filter(Avaliacao.media_geral >= int(rating_filter))

    if date_filter:
        today = datetime.utcnow()
        if date_filter == 'week':
            date_limit = today - timedelta(days=7)
        elif date_filter == 'month':
            date_limit = today - timedelta(days=30)
        elif date_filter == 'year':
            date_limit = today - timedelta(days=365)
        query = query.filter(Avaliacao.data_avaliacao >= date_limit)

    avaliacoes = query.order_by(Avaliacao.data_avaliacao.desc()).all()
    avaliacoes_dict = [avaliacao.to_dict() for avaliacao in avaliacoes]
    return jsonify(avaliacoes=avaliacoes_dict)