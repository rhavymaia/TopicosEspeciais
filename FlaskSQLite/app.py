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
    aluno = request.get_json()
    nome = aluno['nome']
    endereco = aluno['endereco']
    nascimento = aluno['nascimento']
    matricula = aluno['matricula']

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
    aluno["id"] = id

    return jsonify(aluno)

@app.route("/aluno", methods=['PUT'])
def updateAluno():
    print("Atualizar aluno.")
    # Receber o JSON.

    # Buscar o aluno pelo "id".

    # Atualizar os dados caso o aluno seja encontrado através do "id".

    #Retornar o JSON do aluno atualizado.
    return ("PUT", 200)

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
