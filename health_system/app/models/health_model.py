from app.database.connection import DatabaseConnection

class IMCModel:
    def __init__(self, id=None, usuario_id=None, peso=None, altura=None, imc=None, classificacao=None, data_registro=None):
        self.id = id
        self.usuario_id = usuario_id
        self.peso = peso
        self.altura = altura
        self.imc = imc
        self.classificacao = classificacao
        self.data_registro = data_registro

    @staticmethod
    def calcular_classificacao(imc: float) -> str:
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            return "Peso normal"
        elif 25 <= imc < 29.9:
            return "Sobrepeso"
        elif 30 <= imc < 34.9:
            return "Obesidade Grau I"
        elif 35 <= imc < 39.9:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III"

    def salvar(self):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO imc_registos (usuario_id, peso, altura, imc, classificacao)
                VALUES (?, ?, ?, ?, ?);
            """, (self.usuario_id, self.peso, self.altura, self.imc, self.classificacao))
            self.id = cursor.lastrowid

    @classmethod
    def buscar_por_usuario(cls, usuario_id: int):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, peso, altura, imc, classificacao, data_registro
                FROM imc_registos
                WHERE usuario_id = ?
                ORDER BY data_registro DESC;
            """, (usuario_id,))
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]


class RefeicaoModel:
    def __init__(self, id=None, usuario_id=None, titulo=None, descricao=None, calorias=None, data_registro=None):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.descricao = descricao
        self.calorias = calorias
        self.data_registro = data_registro

    def salvar(self):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO refeicoes (usuario_id, titulo, descricao, calorias)
                VALUES (?, ?, ?, ?);
            """, (self.usuario_id, self.titulo, self.descricao, self.calorias))
            self.id = cursor.lastrowid

    @classmethod
    def buscar_por_usuario(cls, usuario_id: int):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, titulo, descricao, calorias, data_registro
                FROM refeicoes
                WHERE usuario_id = ?
                ORDER BY data_registro DESC;
            """, (usuario_id,))
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]