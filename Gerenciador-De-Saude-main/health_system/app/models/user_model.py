from werkzeug.security import generate_password_hash, check_password_hash
from app.database.connection import DatabaseConnection

class UserModel:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    # ----------------------------------------------------
    # MÉTODOS DE INSTÂNCIA (Atuam no objeto específico)
    # ----------------------------------------------------
    def salvar(self):
        """
        Guarda o objeto na base de dados.
        Se self.id for None, cria um novo registo (INSERT).
        Se self.id já existir, atualiza o registo (UPDATE).
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                # Inserção de novo utilizador
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha_hash)
                    VALUES (?, ?, ?);
                """, (self.nome, self.email, self.senha_hash))
                # Captura o ID gerado automaticamente pelo SQLite
                self.id = cursor.lastrowid
            else:
                # Atualização de utilizador existente
                cursor.execute("""
                    UPDATE usuarios
                    SET nome = ?, email = ?, senha_hash = ?
                    WHERE id = ?;
                """, (self.nome, self.email, self.senha_hash, self.id))

    def verificar_senha(self, senha: str) -> bool:
        """Compara a palavra-passe informada com o hash guardado."""
        return check_password_hash(self.senha_hash, senha)

    # ----------------------------------------------------
    # MÉTODOS DE CLASSE (Consultas e Fábrica de Objetos)
    # ----------------------------------------------------
    @classmethod
    def query_filter_by_email(cls, email: str):
        """Procura um utilizador pelo e-mail e devolve uma instância da classe ou None."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, senha_hash 
                FROM usuarios 
                WHERE email = ?;
            """, (email,))
            row = cursor.fetchone()

        if row:
            return cls(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                senha_hash=row['senha_hash']
            )
        return None

    @classmethod
    def buscar_por_id(cls, user_id: int):
        """Procura um utilizador pelo ID e devolve uma instância da classe ou None."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, senha_hash 
                FROM usuarios 
                WHERE id = ?;
            """, (user_id,))
            row = cursor.fetchone()

        if row:
            return cls(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                senha_hash=row['senha_hash']
            )
        return None

    @classmethod
    def criar_usuario(cls, nome: str, email: str, senha: str):
        """
        Cria uma nova instância de UserModel, gera o hash seguro da palavra-passe
        e executa o método salvar() para registar na base de dados.
        """
        senha_hash = generate_password_hash(senha)
        usuario = cls(nome=nome, email=email, senha_hash=senha_hash)
        usuario.salvar()
        return usuario