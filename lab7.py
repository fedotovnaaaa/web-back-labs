from datetime import datetime
from flask import Blueprint, render_template, request, abort, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)


def get_db_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='julia_fedotova_knowledge_base',
        user='julia_fedotova_knowledge_base',
        password='1234567890'
    )


def db_connect():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')


# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)


# Получение одного фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404, description="Фильм с указанным ID не найден")
    
    return jsonify(film)


# Удаление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    
    if not film:
        db_close(conn, cur)
        abort(404, description="Фильм с указанным ID не найден")
    
    # Удаляем фильм
    cur.execute("DELETE FROM films WHERE id = %s", (id,))
    db_close(conn, cur)
    
    return '', 204


# Обновление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    if not cur.fetchone():
        db_close(conn, cur)
        abort(404, description="Фильм с указанным ID не найден")
    
    film = request.get_json()
    
    # Проверка всех полей
    errors = {}
    
    # Проверка русского названия
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Заполните русское название'
    
    # Проверка оригинального названия
    if not film.get('title') or film['title'].strip() == '':
        if not film.get('title_ru') or film['title_ru'].strip() == '':
            errors['title'] = 'Заполните название на оригинальном языке'
        else:
            # Если русское название есть, а оригинального нет - используем русское
            film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        errors['year'] = 'Заполните год выпуска'
    else:
        try:
            year = int(film['year'])
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    if not film.get('description') or film['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    else:
        desc = film['description'].strip()
        if len(desc) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        db_close(conn, cur)
        return jsonify(errors), 400
    
    # Обновляем фильм в БД
    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s 
        WHERE id = %s
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    # Получаем обновленный фильм
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    updated_film = cur.fetchone()
    
    db_close(conn, cur)
    return jsonify(updated_film)


# Создание фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # Проверка всех полей
    errors = {}
    
    # Проверка русского названия
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Заполните русское название'
    
    # Проверка оригинального названия
    if not film.get('title') or film['title'].strip() == '':
        if not film.get('title_ru') or film['title_ru'].strip() == '':
            errors['title'] = 'Заполните название на оригинальном языке'
        else:
            # Если русское название есть, а оригинального нет - используем русское
            film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        errors['year'] = 'Заполните год выпуска'
    else:
        try:
            year = int(film['year'])
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    if not film.get('description') or film['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    else:
        desc = film['description'].strip()
        if len(desc) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    # Вставляем новый фильм
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id
    """, (film['title'], film['title_ru'], film['year'], film['description']))
    
    # Получаем ID нового фильма
    new_id = cur.fetchone()['id']
    
    db_close(conn, cur)
    return jsonify({"id": new_id}), 201
