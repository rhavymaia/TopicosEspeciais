import sqlite3

conn = sqlite3.connect('shallownowschool.db')

cursor = conn.cursor()

cursor.execute("""
    INSERT INTO tb_estudante(nome, endereco,
    nascimento, matricula)
    VALUES('Maria da Conceição', 'Rua da Paz',
    '2019-02-01', '201910010012');
""")

conn.commit()
print("Inserido com sucesso!")

conn.close()
