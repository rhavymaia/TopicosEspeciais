import sqlite3

conn = sqlite3.connect('escola.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE tb_aluno(
        id_aluno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(30) NOT NULL,
        endereco TEXT NOT NULL,
        nascimento DATE NOT NULL,
        matricula VARCHAR(12) NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE tb_curso(
        id_curso INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
    );
""")

cursor.execute("""
    CREATE TABLE tb_disciplina(
        id_disciplina INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
    );
""")

cursor.execute("""
    CREATE TABLE tb_turma(
        id_turma INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
    );
""")

print("Tabelas criadas com sucesso!")
conn.close()
