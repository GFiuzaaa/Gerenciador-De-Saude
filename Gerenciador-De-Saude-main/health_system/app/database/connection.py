import sqlite3

class DatabaseConnection:
    """
    Context Manager para gerir a conexão com a base de dados SQLite.
    Garante o fecho automático da conexão e o commit/rollback de transações.
    """
    def __init__(self, db_name: str = 'saude.db'):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Abre a conexão quando entra no bloco 'with'
        self.conn = sqlite3.connect(self.db_name)
        # Permite aceder aos resultados da consulta como dicionários/objetos (ex: row['nome'])
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                # Se ocorreu algum erro dentro do bloco 'with', desfaz as alterações
                self.conn.rollback()
            else:
                # Se correu tudo bem, guarda as alterações
                self.conn.commit()
            
            # Fecha a conexão automaticamente
            self.conn.close()
        
        # Retorna False para permitir que eventuais erros sejam tratados normalmente
        return False