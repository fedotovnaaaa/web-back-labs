from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'julia_fedotova_knowledge_base',
            user = 'julia_fedotova_knowledge_base',
            password = '1234567890'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else: 
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')

    # проверяет, что все поля заполнены
    if not login or not password or not real_name:
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    # выполняет SQL запрос для поиска пользователя с таким же логином
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    # получает первую строку результата запроса
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', 
                               error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    # Сохранение пользователя в базу
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    # Валидация обязательных полей
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()

    # Поиск пользователя в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    
    # Получение результата запроса
    user = cur.fetchone()

    # Проверка логина, что он есть в БД
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")
    
    # Проверяем, что пароль совпадает
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    # Получение данных из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))    # получает значение чекбокса "Избранное"
    is_public = bool(request.form.get('is_public'))

    # not title.strip() - проверяет, что строка не состоит только из пробелов
    # strip() - удаляет пробелы в начале и конце строки
    if not title or not title.strip():
        return render_template('lab5/create_article.html', error="Тема статьи не может быть пустой")
    
    if not article_text or not article_text.strip():
        return render_template('lab5/create_article.html', error="Текст статьи не может быть пустым")

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]

    # Создание статьи в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) \
                    VALUES (%s, %s, %s, %s, %s);", (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) \
                    VALUES (?, ?, ?, ?, ?);", (user_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/list')
def list():
    login=session.get('login')    # получает логин пользователя из сессии
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    # Получение личных статей пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC;", (user_id, ))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;", (user_id, ))
    
    articles = cur.fetchall()

    # Получение публичных статей всех пользователей
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*, u.login, u.real_name
            FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.id DESC;
        """)
        # SELECT выбирает все поля статей + логин и имя автора
        # FROM объединяет таблицы статей и пользователей
        # WHERE фильтрует только публичные статьи
        # ORDER BY сортирует по ID
    else:
        cur.execute("""
            SELECT a.*, u.login, u.real_name 
            FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.id DESC;
        """)
    
    public_articles = cur.fetchall()
    
    db_close(conn, cur)
    
    # Проверка на пустой список статей
    if not articles:
        return render_template('/lab5/articles.html', articles=articles, public_articles=public_articles, no_articles=True)

    return render_template('/lab5/articles.html', articles=articles, public_articles=public_articles, no_articles=False)



@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']

    # Проверка прав доступа к статье
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена или у вас нет прав для ее редактирования")

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    # Получение новых данных из формы (POST запрос)
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    # Валидация новых данных
    if not title or not title.strip():
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Тема статьи не может быть пустой")
    
    if not article_text or not article_text.strip():
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Текст статьи не может быть пустым")

    # Обновление статьи в базе данных
    # SQL UPDATE запрос - обновляет существующую запись, перечисляет поля для обновления
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s;", 
                   (title, article_text, is_favorite, is_public, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? WHERE id=?;", 
                   (title, article_text, is_favorite, is_public, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']

    # Проверяем, что статья принадлежит пользователю и удаляем
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', real_name=user['real_name'] if user else '')

    # Обработка изменения профиля
    real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Валидация имени
    if not real_name:
        db_close(conn, cur)
        return render_template('lab5/profile.html', error="Имя не может быть пустым")

    # Получаем текущие данные пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()

    # Если пытаются сменить пароль & Валидация полей пароля
    if current_password or new_password or confirm_password:
        if not current_password or not new_password or not confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                   real_name=real_name,
                                   error="Для смены пароля заполните все поля паролей")
        
        # Проверка совпадения новых паролей
        if new_password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                   real_name=real_name,
                                   error="Новый пароль и подтверждение не совпадают")
        
        # Проверка текущего пароля
        if not check_password_hash(user['password'], current_password):
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                   real_name=real_name,
                                   error="Текущий пароль неверен")
        
        # Обновляем пароль
        new_password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", 
                       (real_name, new_password_hash, login))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", 
                       (real_name, new_password_hash, login))
    else:
        # Обновляем только имя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))

    db_close(conn, cur)
    return redirect('/lab5/list')
