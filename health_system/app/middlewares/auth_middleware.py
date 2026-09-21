from flask import session, redirect, url_for, request

def registrar_middlewares(app):
    """Registra todos os middlewares na aplicação Flask."""
    
    @app.before_request
    def verificar_autenticacao():
        # Lista de endpoints/rotas livres que não exigem login
        # Note que agora o endpoint de login é 'auth.login'
        rotas_livres = ['auth.login', 'static']
        
        # Se a rota atual não for livre e o usuário não estiver na sessão
        if request.endpoint and request.endpoint not in rotas_livres:
            if 'usuario_logado' not in session:
                return redirect(url_for('auth.login'))