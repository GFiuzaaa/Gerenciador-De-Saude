from flask import session, redirect, url_for, request

def registrar_middlewares(app):
    """Registra todos os middlewares na aplicação Flask."""
    
    @app.before_request
    def verificar_autenticacao():
        # Liberada a rota 'auth.cadastro'
        rotas_livres = ['auth.login', 'auth.cadastro', 'static']
        
        if request.endpoint and request.endpoint not in rotas_livres:
            if 'usuario_logado' not in session:
                return redirect(url_for('auth.login'))