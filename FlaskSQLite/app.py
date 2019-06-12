from flask import Flask
from flask import request
from flask import jsonify

import sqlite3

# Inicializando a aplicação.
app = Flask(__name__)

DATABASE_NAME = 'escola.db'

@app.route("/alunos")
def getAlunos():
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # executar a consulta.​
    cursor.execute("""
        SELECT * FROM tb_aluno;
    """)

    # iterando os registros.
    alunos = []
    for linha in cursor.fetchall():
        aluno = {
            "id_aluno":linha[0],
            "nome":linha[1],
            "endereco":linha[2],
            "nascimento":linha[3],
            "matricula":linha[4]
        }
        alunos.append(aluno)

    # fechar conexão.
    conn.close()

    return jsonify(alunos)

@app.route("/alunos/<int:id>", methods=['GET'])
def getAluno(id):
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_aluno WHERE id_aluno = ?;
    """, (id, ))

    # iterando os registros.
    #itens = []
    #for linha in cursor.fetchall():
    #    itens.append(dict_factory(linha, cursor))
    linha = cursor.fetchone()
    aluno = {
        "id_aluno":linha[0],
        "nome":linha[1],
        "endereco":linha[2],
        "nascimento":linha[3],
        "matricula":linha[4],
    }

    # fechar conexão.
    conn.close()

    return jsonify(aluno)

@app.route("/aluno", methods=['POST'])
def setAluno():
    # Recuperando dados do JSON.
    json = request.get_json()
    nome = json['nome']
    endereco = json['endereco']
    nascimento = json['nascimento']
    matricula = json['matricula']

    # Inserir dados na Base.
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, endereco, nascimento, matricula)
        VALUES(?, ?, ?, ?);
    """, (nome, endereco, nascimento, matricula))
    conn.commit()
    conn.close()
    # Identificador do último registro inserido.
    id = cursor.lastrowid

    return ("Identificador: %s"%(id), 200)

def dict_factory(linha, cursor):
    dicionario = {}
    for idx, col in enumerate(cursor.description):
        dicionario[col[0]] = linha[idx]
    return dicionario

# Mensagem de erro para recurso não encontrado.
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
