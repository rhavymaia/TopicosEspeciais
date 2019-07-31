import sqlite3

class BancoUtil():

    DATABASE_NAME = 'escola.db'

    def __init__(self):
        # Criar conexão com o Banco de Dados.
        self.conn = BancoUtil.criarConexao()

    def criarConexao():
        # Abrir conexão com o banco de dados.
        conn = sqlite3.connect(BancoUtil.DATABASE_NAME)
        return conn

    def fecharConexao(self):
        print("__exit__")
        cursor = self.conn.cursor()
        cursor.close()
        self.conn.close()

    def listar(self, tabela):
        cursor = self.conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM %s;
        """%(tabela))
        return cursor.fetchall()
