import os
from flask import Flask
from werkzeug.security import generate_password_hash
from app.controllers.auth_controller import auth_bp
from app.middlewares.auth_middleware import registrar_middlewares
from app.database.connection import DatabaseConnection
from app.controllers.health_controller import health_bp
from app.controllers.health_controller import health_bp
from app.database.connection import DatabaseConnection

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')

    # Registo de blueprints e middlewares (registrado apenas uma vez cada)
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    
    registrar_middlewares(app)

    # Inicializa a base de dados com as tabelas e dados iniciais
    _inicializar_banco_sqlite()

    return app

def _inicializar_banco_sqlite():
    """Cria a tabela de utilizadores e insere os registos padrão na primeira execução."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # 1. Criação da tabela (caso ainda não exista)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            );
        """)
                # Tabela de registros de IMC
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS imc_registos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                peso REAL NOT NULL,
                altura REAL NOT NULL,
                imc REAL NOT NULL,
                classificacao TEXT NOT NULL,
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
        """)

        # Tabela de rotinas/refeições
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refeicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                calorias REAL,
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
        """)
        # 2. Verifica se a tabela está vazia
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios;")
        total = cursor.fetchone()['total']

        # 3. Insere os dados iniciais apenas uma vez
        if total == 0:
            usuarios_iniciais = [
                ("João Silva", "joao@teste.com", generate_password_hash("123456")),
                ("Maria Souza", "maria@teste.com", generate_password_hash("senha123"))
            ]
            
            cursor.executemany("""
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (?, ?, ?);
            """, usuarios_iniciais)