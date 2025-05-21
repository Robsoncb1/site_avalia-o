from flask import Blueprint, render_template

# Criar o blueprint
menu_bp = Blueprint('menu', __name__)

# Rota para exibir a página do menu
@menu_bp.route('/menu')
def exibir_menu():
    return render_template('menu.html')
