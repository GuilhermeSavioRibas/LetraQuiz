import pandas as pd
import sqlite3

def migrate_data():
    df = pd.read_excel('perguntas.xlsx')
    df.columns = df.columns.str.strip()

    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO perguntas (tema, pergunta, resposta_correta, resposta_errada_1, resposta_errada_2, resposta_errada_3, material_consulta)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['Tema'], row['Pergunta'], row['Resposta Correta'], row['Resposta Errada 1'], row['Resposta Errada 2'], row['Resposta Errada 3'], row['Material de consulta']))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_data()