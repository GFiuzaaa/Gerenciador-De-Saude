import os
import sqlite3
from flask import Flask
from werkzeug.security import generate_password_hash
from app.controllers.auth_controller import auth_bp
from app.middlewares.auth_middleware import registrar_middlewares

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')

    app.register_blueprint(auth_bp)
    registrar_middlewares(app)

    # Inicializa a base de dados com sqlite3 nativo
    _inicializar_banco_sqlite()

    return app


def _inicializar_banco_sqlite():
    conn = sqlite3.connect('saude.db')
    cursor = conn.cursor()

    # Criação da tabela usando o cursor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        );
    """)
    conn.commit()

    # Verifica se já existem dados
    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    total = cursor.fetchone()[0]

    if total == 0:
        usuarios = [
            ("João Silva", "joao@teste.com", generate_password_hash("123456")),
            ("Maria Souza", "maria@teste.com", generate_password_hash("senha123"))
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (?, ?, ?);
        """, usuarios)
        conn.commit()

    conn.close()