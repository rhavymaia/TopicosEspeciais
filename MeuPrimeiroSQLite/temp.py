import sqlite3

conn = sqlite3.connect('shallownowschool.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE tb_estudante(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(30) NOT NULL,
        endereco TEXT NOT NULL,
        nascimento DATE NOT NULL,
        matricula VARCHAR(12) NOT NULL
    );
""")

print("Tabela tb_estudante criada com sucesso!")
conn.close()



import sqlite3

conn = sqlite3.connect('shallownowschool.db')

cursor = conn.cursor()

valores = [('José', 'Rua Costa Meriz', '2001-02-29', '201610010012')]

cursor.executemany("""
    INSERT INTO tb_estudante(nome, endereco,
    nascimento, matricula)
    VALUES(?, ?, ?, ?);
""", valores)

conn.commit()
print("Valores inseridos com sucesso!")
conn.close()
