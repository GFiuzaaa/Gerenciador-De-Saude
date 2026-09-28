from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = UserModel.query_filter_by_email(email)
        
        if usuario and usuario.verificar_senha(senha):
            session['usuario_logado'] = usuario.email
            session['nome_usuario'] = usuario.nome
            return redirect(url_for('auth.dashboard'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')

    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # 1. Validação de confirmação de senha
        if senha != confirmar_senha:
            flash('As senhas não coincidem!', 'danger')
            return render_template('cadastro.html')

        # 2. Verifica se o e-mail já está registado
        if UserModel.query_filter_by_email(email):
            flash('Este e-mail já está em uso!', 'danger')
            return render_template('cadastro.html')

        # 3. Insere o utilizador na base de dados
        UserModel.criar_usuario(nome, email, senha)
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')

@auth_bp.route('/dashboard')
def dashboard():
    nome = session.get('nome_usuario', 'Usuário')
    return render_template('dashboard.html', nome=nome)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))