from flask import Blueprint, render_template, request, session
import psycopg2


lab6 = Blueprint('lab6', __name__)


# Функция подключения к БД
def get_db_connection():
    return psycopg2.connect(
        host = '127.0.0.1',
        database = 'julia_fedotova_knowledge_base',
        user = 'julia_fedotova_knowledge_base',
        password = '1234567890'
    )



# Получение списка офисов и БД
def get_offices_from_db():
    conn = get_db_connection()
    cur = conn.cursor() # курсор для выполнения SQL-запросов
    cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
    rows = cur.fetchall() # получаем резы запроса
    conn.close()

    offices = []
    for r in rows:
        offices.append({  # добавляем словарь
            "number": r[0],
            "tenant": r[1] if r[1] else "",  # арендатор (если есть) или пустая строка
            "price": r[2]
        })
    return offices



@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


# JSON-RPC API
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json  # Получаем JSON данные из запроса
    req_id = data['id']
    login = session.get('login')
    method = data.get('method')


    # Метод 'info' - получение информации об офисах
    if method == 'info':
        offices = get_offices_from_db() # Получаем все офисы из БД
        if login:
            # показать только свободные и свои
            offices = [o for o in offices if o['tenant'] == '' or o['tenant'] == login]

        return {  # Возвращаем успешный ответ
            "jsonrpc": "2.0",
            "result": offices,  # Список офисов
            "id": req_id  # ID запроса
        }

    # Остальные методы — только для авторизованных
    if not login: # Если пользователь не авторизован
        return {
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Unauthorized"},
            "id": req_id
        }


    # Метод 'booking' - бронирование офиса
    if method == 'booking':
        office_number = data['params']  # Получаем номер офиса из параметров

        conn = get_db_connection()
        cur = conn.cursor()

        # Проверяем существование офиса и текущего арендатора
        cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        row = cur.fetchone()

        if not row:  # Если офис не найден
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 99, "message": "Office not found"},
                "id": req_id
            }

         # Если офис уже занят (tenant не пустой)
        if row[0]:
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Already booked"},
                "id": req_id
            }

        # Бронируем офис для текущего пользователя
        cur.execute("UPDATE offices SET tenant=%s WHERE number=%s", (login, office_number))
        conn.commit()  # Сохраняем изменения в БД
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}


    # Метод 'cancellation' - отмена бронирования
    if method == 'cancellation':
        office_number = data['params']  # Получаем номер офиса

        conn = get_db_connection()
        cur = conn.cursor()

        # Проверяем текущего арендатора
        cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        row = cur.fetchone()

        if not row:  # Офис не найден
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 99, "message": "Office not found"},
                "id": req_id
            }

        # Офис не был арендован
        if row[0] == '':
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 3, "message": "Office is not rented"},
                "id": req_id
            }

        # офис снят другим пользователем
        if row[0] != login:
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 4, "message": "Cannot cancel someone else's rental"},
                "id": req_id
            }

        # Освобождаем офис (устанавливаем tenant в пустую строку)
        cur.execute("UPDATE offices SET tenant='' WHERE number=%s", (office_number,))
        conn.commit()
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    # Обработка неизвестного метода
    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": req_id
    }
