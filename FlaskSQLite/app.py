from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
import sqlite3
import logging

from entidade.Aluno import Aluno
from dao.AlunoDAO import AlunoDAO

# Inicializando a aplicação.
app = Flask(__name__)

# Logging
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("escolaapp.log")
handler.setFormatter(formatter)

logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Validação
schema = JsonSchema()
schema.init_app(app)

aluno_schema = {
    'required': ['nome', 'endereco', 'nascimento', 'matricula'],
    'properties': {
        'nome': {'type': 'string'},
        'endereco': {'type': 'string'},
        'nascimento': {'type': 'string'},
        'matricula': {'type': 'string'},
    }
}

# Banco de dados.
DATABASE_NAME = 'escola_2.db'

@app.route("/alunos")
def getAlunos():
    logger.info("Listando alunos.")

    try:
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
        logger.info(alunos)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro.")

    return jsonify(alunos)

@app.route("/alunos/<int:id>", methods=['GET'])
def getAluno(id):
    logger.info("Listando aluno por id: %s"%(id))
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
@schema.validate(aluno_schema)
def setAluno():
    # Recuperando dados do JSON.
    alunoJson = request.get_json()
    nome = alunoJson['nome']
    endereco = alunoJson['endereco']
    nascimento = alunoJson['nascimento']
    matricula = alunoJson['matricula']
    aluno = Aluno(nome, endereco, nascimento, matricula)

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

@app.route("/aluno/<int:id>", methods=['PUT'])
def updateAluno(id):
    # Receber o JSON.
    aluno = request.get_json()
    nome = aluno['nome']
    endereco = aluno['endereco']
    nascimento = aluno['nascimento']
    matricula = aluno['matricula']

    # Buscar o aluno pelo "id".
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_aluno WHERE id_aluno = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:
        # Atualizar os dados caso o aluno seja encontrado através do "id".
        cursor.execute("""
            UPDATE tb_aluno
            SET nome=?, endereco=?, nascimento=?, matricula=?
            WHERE id_aluno = ?;
        """, (nome, endereco, nascimento, matricula, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_aluno(nome, endereco, nascimento, matricula)
            VALUES(?, ?, ?, ?);
        """, (nome, endereco, nascimento, matricula))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        aluno["id"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(aluno)

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

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})


if(__name__ == '__main__'):
    #dao = AlunoDAO()
    #print(dao.listar())

    app.run(host='0.0.0.0', debug=True, use_reloader=True)
