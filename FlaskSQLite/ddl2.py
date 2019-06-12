import sqlite3

conn = sqlite3.connect('escola2.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE tb_aluno (
        id_aluno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        matricula VARCHAR(12) NOT NULL,
        cpf VARCHAR(11) NOT NULL,
        nascimento DATE NOT NULL
    );
""")
print("Tabela tb_aluno foi criada.")

cursor.execute("""
    CREATE TABLE tb_curso (
        id_curso INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        turno VARCHAR(1) NOT NULL
    );
""")
print("Tabela tb_curso foi criada.")

cursor.execute("""
    CREATE TABLE tb_turma (
        id_turma INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        fk_id_curso INTEGER NOT NULL
    );
""")
print("Tabela tb_turma foi criada.")

conn.close()
