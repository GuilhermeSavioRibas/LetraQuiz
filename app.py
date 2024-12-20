from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from datetime import datetime
import sqlite3
import random
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    """Render the index page with available quiz themes."""
    error = session.pop('error', None)
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tema FROM perguntas")
        temas = [row['tema'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        temas = []
    finally:
        conn.close()
    return render_template('index.html', temas=temas, top5=[], error=error)

@app.route('/start_quiz', methods=['POST'])
@login_required
def start_quiz():
    tema = request.form['tema']
    if not tema:
        return redirect(url_for('index', error='Selecione um tema'))
    usuario = request.form['usuario']
    session['tema'] = tema
    session['usuario'] = usuario
    session['score'] = 0
    session['pulos'] = 3
    session['consultas_l2'] = 1
    session['cartas'] = 1
    session['consultas_artigo'] = 1
    session['answered_questions'] = []
    return render_template('quiz.html', tema=tema, usuario=usuario)

@app.route('/get_question', methods=['POST'])
@login_required
def get_question():
    tema = session.get('tema').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perguntas WHERE TRIM(tema) = ? ORDER BY RANDOM()", (tema,))
    perguntas_tema = cursor.fetchall()
    conn.close()

    if not perguntas_tema:
        return jsonify({'error': 'Nenhuma pergunta encontrada para esse tema.'}), 404

    answered_questions = session.get('answered_questions', [])
    perguntas_restantes = [p for p in perguntas_tema if p['id'] not in answered_questions]

    if not perguntas_restantes:
        save_score()
        return jsonify({'success': 'Você ganhou! Todas as perguntas foram respondidas.'}), 200

    pergunta = random.choice(perguntas_restantes)
    session['answered_questions'].append(pergunta['id'])
    opcoes = [
        pergunta['resposta_correta'],
        pergunta['resposta_errada_1'],
        pergunta['resposta_errada_2'],
        pergunta['resposta_errada_3']
    ]
    random.shuffle(opcoes)
    session['correct_answer'] = pergunta['resposta_correta']
    session['artigo'] = pergunta['material_consulta'] if pergunta['material_consulta'] else None
    session['current_question'] = pergunta['pergunta']
    session['current_options'] = opcoes

    total_perguntas = len(perguntas_tema)
    pergunta_numero = len(session['answered_questions'])

    return jsonify({
        'pergunta': pergunta['pergunta'],
        'opcoes': opcoes,
        'tema': tema,
        'usuario': session.get('usuario'),
        'score': session.get('score'),
        'pulos': session.get('pulos'),
        'consultas_l2': session.get('consultas_l2'),
        'cartas': session.get('cartas'),
        'consultas_artigo': session.get('consultas_artigo'),
        'artigo': session['artigo'],
        'total_perguntas': total_perguntas,
        'pergunta_numero': pergunta_numero
    })

@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    resposta = request.form['resposta']
    correct_answer = session.get('correct_answer')
    current_question = session.get('current_question')
    if resposta == correct_answer:
        session['score'] += 1
        return jsonify({'correct': True})
    else:
        save_score()
        return jsonify({'correct': False, 'score': session.get('score'), 'question': current_question, 'correct_answer': correct_answer})

@app.route('/use_skip', methods=['POST'])
@login_required
def use_skip():
    if session['pulos'] > 0:
        session['pulos'] -= 1
        return jsonify({'success': True, 'pulos': session['pulos']})
    return jsonify({'success': False})

@app.route('/use_l2', methods=['POST'])
@login_required
def use_l2():
    if session['consultas_l2'] > 0:
        session['consultas_l2'] -= 1
        return jsonify({'success': True, 'consultas_l2': session['consultas_l2']})
    return jsonify({'success': False})

@app.route('/use_card', methods=['POST'])
@login_required
def use_card():
    if session['cartas'] > 0:
        session['cartas'] -= 1
        cartas = ['0', '1', '2', '3']
        carta_escolhida = random.choice(cartas)

        opcoes = session.get('current_options')
        correct_answer = session.get('correct_answer')
        respostas_erradas = [opcao for opcao in opcoes if opcao != correct_answer]

        if carta_escolhida == '0':
            pass
        elif carta_escolhida == '1' and len(respostas_erradas) >= 1:
            respostas_erradas = respostas_erradas[:2]
        elif carta_escolhida == '2' and len(respostas_erradas) >= 2:
            respostas_erradas = respostas_erradas[:1]
        elif carta_escolhida == '3':
            respostas_erradas = respostas_erradas[:0]

        novas_opcoes = [correct_answer] + respostas_erradas
        random.shuffle(novas_opcoes)

        session['current_options'] = novas_opcoes

        carta_imagem = f"static/images/card{carta_escolhida}.png"

        return jsonify({'success': True, 'carta': carta_escolhida, 'carta_imagem': carta_imagem, 'opcoes': novas_opcoes, 'cartas': session['cartas'], 'pergunta': session['current_question']})
    return jsonify({'success': False})

@app.route('/use_article', methods=['POST'])
@login_required
def use_article():
    if session['consultas_artigo'] > 0:
        session['consultas_artigo'] -= 1
        artigo = session.get('artigo')
        if artigo:
            return jsonify({'success': True, 'artigo': artigo, 'consultas_artigo': session['consultas_artigo']})
        else:
            return jsonify({'success': False, 'message': 'Nenhum artigo disponível para esta questão.'})
    return jsonify({'success': False})

@app.route('/get_article', methods=['GET'])
@login_required
def get_article():
    artigo = session.get('artigo')
    return jsonify({'artigo': artigo})

@app.route('/end_quiz', methods=['POST'])
@login_required
def end_quiz():
    save_score()
    return redirect('/')

@app.route('/get_top5', methods=['GET'])
@login_required
def get_top5_route():
    tema = request.args.get('tema')
    if tema:
        tema = tema.strip()
    top5 = get_top5(tema)
    return jsonify(top5)

def get_top5(tema=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if tema:
        cursor.execute("SELECT * FROM resultados WHERE TRIM(tema) = ? ORDER BY score DESC LIMIT 5", (tema,))
    else:
        cursor.execute("SELECT * FROM resultados ORDER BY score DESC LIMIT 5")
    top5 = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return top5

def save_score():
    usuario = session.get('usuario')
    score = session.get('score')
    tema = session.get('tema')
    quiz_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resultados (usuario, score, tema, data) VALUES (?, ?, ?, ?)", (usuario, score, tema, quiz_date))
    conn.commit()
    conn.close()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = ?", (login,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['user_type'] = user['tipo_usuario'].strip()
            next_page = session.pop('next', url_for('index'))
            if is_safe_url(next_page):
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            session['error'] = 'Credenciais inválidas'
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session['user_type'] != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/questions', methods=['GET'])
@login_required
@admin_required
def admin_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perguntas")
    questions = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT tema FROM perguntas")
    themes = [row['tema'] for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM usuarios")
    users = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return render_template('admin_questions.html', questions=questions, themes=themes, users=users)

@app.route('/admin/add_theme_questions', methods=['GET', 'POST'])
@login_required
@admin_required
def add_theme_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT tema FROM perguntas")
    existing_themes = [row['tema'] for row in cursor.fetchall()]
    conn.close()
    
    if request.method == 'POST':
        theme_select = request.form['theme-select']
        if theme_select == 'new':
            theme = request.form['new_theme']
            if not theme:
                return render_template('add_theme_questions.html', existing_themes=existing_themes, error='Por favor, insira um nome para o novo tema.')
        elif theme_select == '':
            return render_template('add_theme_questions.html', existing_themes=existing_themes, error='Por favor, selecione um tema existente ou escolha criar um novo.')
        else:
            theme = theme_select
        questions = []
        for i in range(1, 100):
            question = request.form.get(f'question_{i}')
            if not question:
                break
            resposta_correta = request.form.get(f'resposta_correta_{i}')
            resposta_errada1 = request.form.get(f'resposta_errada1_{i}')
            resposta_errada2 = request.form.get(f'resposta_errada2_{i}')
            resposta_errada3 = request.form.get(f'resposta_errada3_{i}')
            material_consulta = request.form.get(f'material_consulta_{i}')
            questions.append({
                'question': question,
                'resposta_correta': resposta_correta,
                'resposta_errada1': resposta_errada1,
                'resposta_errada2': resposta_errada2,
                'resposta_errada3': resposta_errada3,
                'material_consulta': material_consulta
            })
        if not questions:
            return render_template('add_theme_questions.html', existing_themes=existing_themes, error='Por favor, adicione pelo menos uma pergunta.')
        save_theme_and_questions(theme, questions)
        return redirect(url_for('admin_questions'))
    return render_template('add_theme_questions.html', existing_themes=existing_themes)

def save_theme_and_questions(theme, questions):
    conn = get_db_connection()
    cursor = conn.cursor()
    for q in questions:
        cursor.execute("""
            INSERT INTO perguntas (tema, pergunta, resposta_correta, resposta_errada_1, resposta_errada_2, resposta_errada_3, material_consulta)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (theme, q['question'], q['resposta_correta'], q['resposta_errada1'], q['resposta_errada2'], q['resposta_errada3'], q['material_consulta']))
    conn.commit()
    conn.close()

@app.route('/admin/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perguntas WHERE id = ?", (question_id,))
    question = cursor.fetchone()
    conn.close()
    if not question:
        return redirect(url_for('admin_questions'))
    if request.method == 'POST':
        tema = request.form['tema']
        pergunta = request.form['pergunta']
        resposta_correta = request.form['resposta_correta']
        resposta_errada1 = request.form['resposta_errada1']
        resposta_errada2 = request.form['resposta_errada2']
        resposta_errada3 = request.form['resposta_errada3']
        material_consulta = request.form['material_consulta']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE perguntas SET
            tema = ?,
            pergunta = ?,
            resposta_correta = ?,
            resposta_errada_1 = ?,
            resposta_errada_2 = ?,
            resposta_errada_3 = ?,
            material_consulta = ?
            WHERE id = ?
        """, (tema, pergunta, resposta_correta, resposta_errada1, resposta_errada2, resposta_errada3, material_consulta, question_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_questions'))
    return render_template('edit_question.html', question=question)

@app.route('/admin/delete_question/<int:question_id>', methods=['GET'])
@login_required
@admin_required
def delete_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM perguntas WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_questions'))


@app.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def admin_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('admin_users.html', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        tipo_usuario = request.form['tipo_usuario']
        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (login, senha, tipo_usuario) VALUES (?, ?, ?)", (login, hashed_password, tipo_usuario))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_users'))
    return render_template('add_user.html')

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return redirect(url_for('admin_users'))
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        tipo_usuario = request.form['tipo_usuario']
        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios SET
            login = ?,
            senha = ?,
            tipo_usuario = ?
            WHERE id = ?
        """, (login, hashed_password, tipo_usuario, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_users'))
    return render_template('edit_user.html', user=user)

@app.route('/admin/delete_user/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_users'))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)


    # implementar tela de cadastro de usuários
    # implementar recursos de acessibilidade
