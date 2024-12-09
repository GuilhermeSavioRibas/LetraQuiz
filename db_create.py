import sqlite3

def create_database():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS perguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema TEXT NOT NULL,
        pergunta TEXT NOT NULL,
        resposta_correta TEXT NOT NULL,
        resposta_errada_1 TEXT NOT NULL,
        resposta_errada_2 TEXT NOT NULL,
        resposta_errada_3 TEXT NOT NULL,
        material_consulta TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        score INTEGER NOT NULL,
        tema TEXT NOT NULL,
        data TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL DEFAULT 'normal'
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()