from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    # Lista simulada contendo apenas usuários comuns
    _tabela_usuarios_mock = [
        {
            "id": 1,
            "email": "joao@teste.com",
            "nome": "João Silva",
            "senha_hash": generate_password_hash("123456")
        },
        {
            "id": 2,
            "email": "maria@teste.com",
            "nome": "Maria Souza",
            "senha_hash": generate_password_hash("senha123")
        }
    ]

    def __init__(self, id, email, nome, senha_hash):
        self.id = id
        self.email = email
        self.nome = nome
        self.senha_hash = senha_hash

    @classmethod
    def query_filter_by_email(cls, email):
        """Busca o usuário simulando o SQLAlchemy."""
        for u in cls._tabela_usuarios_mock:
            if u["email"] == email:
                return cls(u["id"], u["email"], u["nome"], u["senha_hash"])
        return None

    def verificar_senha(self, senha):
        """Verifica se a senha confere."""
        return check_password_hash(self.senha_hash, senha)