import sqlite3
from dao.BancoUtil import BancoUtil

class AlunoDAO():
    # Nome da tabela.
    TB_NAME = "tb_aluno"

    def __init__(self):
        # Prepara a conexão do BD.
        self.banco = BancoUtil()

    def listar(self):
        # Recupera os dados da consultar em formato de tupla.
        registros = self.banco.listar(AlunoDAO.TB_NAME)
        alunos = []
        for linha in registros:
            aluno = {
                "id_aluno":linha[0],
                "nome":linha[1],
                "endereco":linha[2],
                "nascimento":linha[3],
                "matricula":linha[4]
            }
            alunos.append(aluno)
        # Fechar conexão.
        self.banco.fecharConexao()
        return alunos

    def inserir(self):
        pass
