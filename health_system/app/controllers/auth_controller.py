from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Rota raiz redireciona dependendo se o usuário está logado ou não."""
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona direto para o dashboard
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Busca o usuário usando o padrão estilo ORM do model
        usuario = UserModel.query_filter_by_email(email)
        
        # Valida o usuário e a senha
        if usuario and usuario.verificar_senha(senha):
            session['usuario_logado'] = usuario.email
            session['nome_usuario'] = usuario.nome
            return redirect(url_for('auth.dashboard'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')

    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    # Protegido automaticamente pelo middleware, mas garantimos a extração do nome
    nome = session.get('nome_usuario', 'Usuário')
    return render_template('dashboard.html', nome=nome)

@auth_bp.route('/logout')
def logout():
    # Limpa a sessão para encerrar o login
    session.clear()
    return redirect(url_for('auth.login'))