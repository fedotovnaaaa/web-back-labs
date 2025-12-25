from flask import Blueprint, request, jsonify, session, render_template
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash  # ← ИМПОРТИРУЕМ ЭТО
import os
import re

rgz = Blueprint('rgz', __name__)

def get_db_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='julia_fedotova_knowledge_base',
        user='julia_fedotova_knowledge_base',
        password='1234567890'
    )

def db_conn():
    conn = get_db_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Главная страница
@rgz.route('/rgz/')
def index():
    return render_template('rgz/index.html')


# API: Авторизация
@rgz.route('/rgz/rest-api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    login = data.get('login', '').strip()
    password = data.get('password', '').strip()

    if not login or not password:
        return jsonify({'error': 'Логин и пароль обязательны'}), 400

    conn, cur = db_conn()
    cur.execute("SELECT * FROM users_rgz WHERE login = %s", (login,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Неверный логин или пароль'}), 401

    session['user_id']   = user['id']
    session['role']      = user['role']
    session['full_name'] = user['full_name']

    return jsonify({
        'id': user['id'],
        'full_name': user['full_name'],
        'role': user['role'],
        'phone': user.get('phone')
    })

@rgz.route('/rgz/rest-api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Выход выполнен'})


# API: Клиент — данные счёта
@rgz.route('/rgz/rest-api/client/account/<int:user_id>', methods=['GET'])
def get_account(user_id):
    if 'user_id' not in session or session['user_id'] != user_id or session['role'] != 'client':
        return jsonify({'error': 'Доступ запрещён'}), 403

    conn, cur = db_conn()
    cur.execute("""
        SELECT acc.account_number, acc.balance 
        FROM accounts_rgz acc 
        JOIN users_rgz u ON u.id = acc.user_id 
        WHERE u.id = %s
    """, (user_id,))
    account = cur.fetchone()
    db_close(conn, cur)

    if not account:
        return jsonify({'error': 'Счёт не найден'}), 404

    return jsonify(account)


# API: Клиент — история операций
@rgz.route('/rgz/rest-api/client/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    if 'user_id' not in session or session['user_id'] != user_id or session['role'] != 'client':
        return jsonify({'error': 'Доступ запрещён'}), 403

    conn, cur = db_conn()
    cur.execute("""
        SELECT 
            t.id,
            CASE WHEN t.from_user_id = %s THEN u_to.full_name ELSE u_from.full_name END AS counterparty,
            CASE WHEN t.from_user_id = %s THEN 'Расход' ELSE 'Доход' END AS type,
            t.amount,
            t.created_at
        FROM transactions_rgz t
        JOIN users_rgz u_from ON t.from_user_id = u_from.id
        JOIN users_rgz u_to ON t.to_user_id = u_to.id
        WHERE t.from_user_id = %s OR t.to_user_id = %s
        ORDER BY t.created_at DESC
    """, (user_id, user_id, user_id, user_id))
    rows = cur.fetchall()
    db_close(conn, cur)

    return jsonify(rows)


# API: Клиент — перевод
@rgz.route('/rgz/rest-api/client/transfer', methods=['POST'])
def client_transfer():
    if 'user_id' not in session or session['role'] != 'client':
        return jsonify({'error': 'Доступ запрещён'}), 403

    data = request.get_json()
    to_identifier = data.get('to_account', '').strip()
    amount = data.get('amount')

    if not to_identifier:
        return jsonify({'error': 'Укажите номер счёта или телефон получателя'}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Сумма должна быть положительным числом'}), 400

    if amount > 1000000:
        return jsonify({'error': 'Максимальная сумма перевода — 1 000 000'}), 400

    conn, cur = db_conn()

    cur.execute("""
        SELECT acc.id AS account_id, acc.balance, u.id AS user_id 
        FROM accounts_rgz acc 
        JOIN users_rgz u ON u.id = acc.user_id 
        WHERE u.id = %s
    """, (session['user_id'],))
    sender = cur.fetchone()

    if sender['balance'] < amount:
        db_close(conn, cur)
        return jsonify({'error': 'Недостаточно средств'}), 400

    cur.execute("""
        SELECT u.id AS user_id, acc.id AS account_id, u.full_name, acc.balance
        FROM users_rgz u
        JOIN accounts_rgz acc ON acc.user_id = u.id
        WHERE (acc.account_number = %s OR u.phone = %s)
          AND u.role = 'client'
          AND u.id != %s
    """, (to_identifier, to_identifier, session['user_id']))
    receiver = cur.fetchone()

    if not receiver:
        db_close(conn, cur)
        return jsonify({'error': 'Получатель не найден'}), 404

    cur.execute("UPDATE accounts_rgz SET balance = balance - %s WHERE id = %s", (amount, sender['account_id']))
    cur.execute("UPDATE accounts_rgz SET balance = balance + %s WHERE id = %s", (amount, receiver['account_id']))

    cur.execute("""
        INSERT INTO transactions_rgz (from_user_id, to_user_id, amount, created_at)
        VALUES (%s, %s, %s, %s)
    """, (session['user_id'], receiver['user_id'], amount, datetime.now()))

    db_close(conn, cur)

    return jsonify({'message': 'Перевод успешен'})


# API: Менеджер — список пользователей + фильтр по телефону
@rgz.route('/rgz/rest-api/manager/users', methods=['GET'])
def manager_get_users():
    if 'role' not in session or session['role'] != 'manager':
        return jsonify({'error': 'Доступ запрещён'}), 403

    phone_filter = request.args.get('phone', '').strip()

    conn, cur = db_conn()

    if phone_filter:
        # Поиск по точному номеру телефона
        cur.execute("""
            SELECT u.id, u.full_name, u.login, u.phone, u.role,
                   acc.account_number, acc.balance
            FROM users_rgz u
            LEFT JOIN accounts_rgz acc ON acc.user_id = u.id
            WHERE u.phone = %s
            ORDER BY u.full_name
        """, (phone_filter,))
    else:
        # Все пользователи
        cur.execute("""
            SELECT u.id, u.full_name, u.login, u.phone, u.role,
                   acc.account_number, acc.balance
            FROM users_rgz u
            LEFT JOIN accounts_rgz acc ON acc.user_id = u.id
            ORDER BY u.full_name
        """)

    users = cur.fetchall()
    db_close(conn, cur)

    return jsonify(users)


# API: Менеджер — создание пользователя
@rgz.route('/rgz/rest-api/manager/user', methods=['POST'])
def manager_create_user():
    if session.get('role') != 'manager':
        return jsonify({'error': 'Доступ запрещён'}), 403

    data = request.get_json()

    required = ['full_name', 'login', 'password', 'role']
    for field in required:
        if field not in data or not str(data[field]).strip():
            return jsonify({'error': f'Поле {field} обязательно'}), 400

    full_name = data['full_name'].strip()
    login = data['login'].strip()
    password = data['password']
    phone = data.get('phone', '').strip()
    role = data['role']

    if role not in ['client', 'manager']:
        return jsonify({'error': 'Недопустимая роль'}), 400

    # Валидация
    if len(full_name) < 2 or len(full_name) > 100:
        return jsonify({'error': 'ФИО должно быть от 2 до 100 символов'}), 400

    if len(login) < 3 or len(login) > 50:
        return jsonify({'error': 'Логин должен быть от 3 до 50 символов'}), 400

    if not re.match(r'^[a-zA-Z0-9_.-]+$', login):
        return jsonify({'error': 'Логин может содержать только латинские буквы, цифры, _, . и -'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Пароль должен быть не короче 6 символов'}), 400

    # Проверка телефона: строго +7 + 10 цифр (всего 11 цифр после +)
    if phone:
        if not re.match(r'^\+7\d{10}$', phone):
            return jsonify({'error': 'Номер телефона должен начинаться с +7 и содержать ровно 10 цифр после +7'}), 400

    if role == 'client':
        account_number = data.get('account_number', '').strip()
        balance = data.get('balance')

        if not account_number or not re.match(r'^\d{20}$', account_number):
            return jsonify({'error': 'Номер счёта должен состоять ровно из 20 цифр'}), 400

        try:
            balance = float(balance)
            if balance < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Баланс должен быть числом ≥ 0'}), 400

    conn, cur = db_conn()

    # Проверка уникальности логина
    cur.execute("SELECT 1 FROM users_rgz WHERE login = %s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({'error': 'Логин уже занят'}), 409

    # Проверка уникальности телефона (если указан)
    if phone:
        cur.execute("SELECT 1 FROM users_rgz WHERE phone = %s", (phone,))
        if cur.fetchone():
            db_close(conn, cur)
            return jsonify({'error': 'Номер телефона уже занят'}), 409

    # Проверка уникальности номера счёта (для клиента)
    if role == 'client':
        cur.execute("SELECT 1 FROM accounts_rgz WHERE account_number = %s", (account_number,))
        if cur.fetchone():
            db_close(conn, cur)
            return jsonify({'error': 'Номер счёта уже занят'}), 409

    # Хэшируем пароль
    password_hash = generate_password_hash(password)

    cur.execute("""
        INSERT INTO users_rgz (full_name, login, password_hash, phone, role)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (full_name, login, password_hash, phone, role))

    user_id = cur.fetchone()['id']

    if role == 'client':
        cur.execute("""
            INSERT INTO accounts_rgz (user_id, account_number, balance)
            VALUES (%s, %s, %s)
        """, (user_id, account_number, balance))

    db_close(conn, cur)

    return jsonify({'message': 'Пользователь создан', 'id': user_id}), 201


# API: Менеджер — обновление пользователя
@rgz.route('/rgz/rest-api/manager/user/<int:user_id>', methods=['PUT'])
def manager_update_user(user_id):
    if session.get('role') != 'manager':
        return jsonify({'error': 'Доступ запрещён'}), 403

    data = request.get_json()

    conn, cur = db_conn()

    cur.execute("SELECT * FROM users_rgz WHERE id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return jsonify({'error': 'Пользователь не найден'}), 404

    updates = []
    params = []

    if 'full_name' in data:
        full_name = data['full_name'].strip()
        if len(full_name) < 2 or len(full_name) > 100:
            db_close(conn, cur)
            return jsonify({'error': 'ФИО должно быть от 2 до 100 символов'}), 400
        updates.append("full_name = %s")
        params.append(full_name)

    if 'login' in data:
        login = data['login'].strip()
        if len(login) < 3 or len(login) > 50:
            db_close(conn, cur)
            return jsonify({'error': 'Логин должен быть от 3 до 50 символов'}), 400
        if not re.match(r'^[a-zA-Z0-9_.-]+$', login):
            db_close(conn, cur)
            return jsonify({'error': 'Недопустимые символы в логине'}), 400
        cur.execute("SELECT 1 FROM users_rgz WHERE login = %s AND id != %s", (login, user_id))
        if cur.fetchone():
            db_close(conn, cur)
            return jsonify({'error': 'Логин занят'}), 409
        updates.append("login = %s")
        params.append(login)

    if 'password' in data:
        password = data['password']
        if len(password) < 6:
            db_close(conn, cur)
            return jsonify({'error': 'Пароль должен быть не короче 6 символов'}), 400
        password_hash = generate_password_hash(password)
        updates.append("password_hash = %s")
        params.append(password_hash)

    if 'phone' in data:
        phone = data['phone'].strip()
        if phone:  # если телефон указан
            if not re.match(r'^\+7\d{10}$', phone):
                db_close(conn, cur)
                return jsonify({'error': 'Номер телефона должен начинаться с +7 и содержать ровно 10 цифр после +7'}), 400
            cur.execute("SELECT 1 FROM users_rgz WHERE phone = %s AND id != %s", (phone, user_id))
            if cur.fetchone():
                db_close(conn, cur)
                return jsonify({'error': 'Номер телефона уже занят'}), 409
        updates.append("phone = %s")
        params.append(phone)

    if 'role' in data and data['role'] in ['client', 'manager']:
        updates.append("role = %s")
        params.append(data['role'])

    if updates:
        query = "UPDATE users_rgz SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(user_id)
        cur.execute(query, params)

    # Обновление счёта клиента
    if user['role'] == 'client':
        cur.execute("SELECT * FROM accounts_rgz WHERE user_id = %s", (user_id,))
        account = cur.fetchone()
        if account:
            acc_updates = []
            acc_params = []

            if 'account_number' in data:
                acc_num = data['account_number'].strip()
                if not re.match(r'^\d{20}$', acc_num):
                    db_close(conn, cur)
                    return jsonify({'error': 'Номер счёта должен состоять из 20 цифр'}), 400
                cur.execute("SELECT 1 FROM accounts_rgz WHERE account_number = %s AND user_id != %s", (acc_num, user_id))
                if cur.fetchone():
                    db_close(conn, cur)
                    return jsonify({'error': 'Номер счёта занят'}), 409
                acc_updates.append("account_number = %s")
                acc_params.append(acc_num)

            if 'balance' in data:
                try:
                    balance = float(data['balance'])
                    if balance < 0:
                        raise ValueError
                    acc_updates.append("balance = %s")
                    acc_params.append(balance)
                except (ValueError, TypeError):
                    db_close(conn, cur)
                    return jsonify({'error': 'Баланс должен быть числом ≥ 0'}), 400

            if acc_updates:
                acc_query = "UPDATE accounts_rgz SET " + ", ".join(acc_updates) + " WHERE user_id = %s"
                acc_params.append(user_id)
                cur.execute(acc_query, acc_params)

    db_close(conn, cur)
    return jsonify({'message': 'Данные обновлены'})


# API: Менеджер — удаление пользователя
@rgz.route('/rgz/rest-api/manager/user/<int:user_id>', methods=['DELETE'])
def manager_delete_user(user_id):
    if session.get('role') != 'manager':
        return jsonify({'error': 'Доступ запрещён'}), 403

    if session['user_id'] == user_id:
        return jsonify({'error': 'Нельзя удалить самого себя'}), 403

    conn, cur = db_conn()
    cur.execute("SELECT * FROM users_rgz WHERE id = %s", (user_id,))
    if not cur.fetchone():
        db_close(conn, cur)
        return jsonify({'error': 'Пользователь не найден'}), 404

    cur.execute("DELETE FROM users_rgz WHERE id = %s", (user_id,))
    db_close(conn, cur)

    return jsonify({'message': 'Пользователь удалён'})
