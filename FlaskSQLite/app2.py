from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/alunos", methods=['GET'])
def getAlunos():
    conn = sqlite3.connect('escola2.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_aluno;
    """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()
    return ("Executado", 200)

@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunosByID(id):
    pass

@app.route("/aluno", methods=['POST'])
def setAluno():
    nome = request.form["nome"]
    nascimento = request.form["nascimento"]
    matricula = request.form["matricula"]
    cpf = request.form["cpf"]
    conn = sqlite3.connect("escola2.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento)
        VALUES(?, ?, ?, ?);
    """, (nome, matricula, cpf, nascimento))
    conn.commit()
    conn.close()

    return ('Cadastrado com sucesso', 200)

def getCursos():
    pass

def getCursosByID(id):
    pass

def getTurmas():
    pass

def getTurmasByID(id):
    pass

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
