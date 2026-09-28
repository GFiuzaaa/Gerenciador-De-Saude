import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    @classmethod
    def query_filter_by_email(cls, email: str):
        conn = sqlite3.connect('saude.db')
        cursor = conn.cursor()

        query = f"SELECT id, nome, email, senha_hash FROM usuarios WHERE email = '{email}'"
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return cls(
                id=resultado[0],
                nome=resultado[1],
                email=resultado[2],
                senha_hash=resultado[3]
            )
        return None

    @classmethod
    def criar_usuario(cls, nome: str, email: str, senha: str):
        """Insere um novo utilizador na base de dados usando o cursor."""
        conn = sqlite3.connect('saude.db')
        cursor = conn.cursor()

        # Gera o hash seguro da palavra-passe antes de salvar
        senha_hash = generate_password_hash(senha)

        # Executa a inserção parametrizada
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (?, ?, ?);
        """, (nome, email, senha_hash))

        conn.commit()
        conn.close()

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)