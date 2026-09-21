from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.middlewares.auth_middleware import registrar_middlewares

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.config['SECRET_KEY'] = 'sua-chave-secreta-super-segura-aqui'
    
    # Configuração futura para o Flask-SQLAlchemy (exemplo)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saude.db'

    # Registrando o Blueprint de Autenticação
    app.register_blueprint(auth_bp)

    # Registrando os middlewares da aplicação
    registrar_middlewares(app)

    return app