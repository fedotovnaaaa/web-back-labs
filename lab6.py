from flask import Blueprint, render_template, request, session
import psycopg2


lab6 = Blueprint('lab6', __name__)


# ---- ФУНКЦИЯ ПОДКЛЮЧЕНИЯ К БД ----
def get_db_connection():
    return psycopg2.connect(
        host = '127.0.0.1',
        database = 'julia_fedotova_knowledge_base',
        user = 'julia_fedotova_knowledge_base',
        password = '1234567890'
    )



# ---- ПОЛУЧЕНИЕ СПИСКА ОФИСОВ ИЗ БД ----
def get_offices_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
    rows = cur.fetchall()
    conn.close()

    offices = []
    for r in rows:
        offices.append({
            "number": r[0],
            "tenant": r[1] if r[1] else "",
            "price": r[2]
        })
    return offices


# ---- ОТДАЁМ СТРАНИЦУ ----
@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


# ---- JSON-RPC API ----
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    req_id = data['id']
    login = session.get('login')
    method = data.get('method')


    if method == 'info':
        offices = get_offices_from_db()
        if login:
            # показать только свободные и свои
            offices = [o for o in offices if o['tenant'] == '' or o['tenant'] == login]

        return {
            "jsonrpc": "2.0",
            "result": offices,
            "id": req_id
        }

    # Остальные методы — только для авторизованных
    if not login:
        return {
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Unauthorized"},
            "id": req_id
        }


    if method == 'booking':
        office_number = data['params']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        row = cur.fetchone()

        if not row:
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 99, "message": "Office not found"},
                "id": req_id
            }

        # уже занято
        if row[0]:
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Already booked"},
                "id": req_id
            }

        # бронируем
        cur.execute("UPDATE offices SET tenant=%s WHERE number=%s", (login, office_number))
        conn.commit()
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}


    if method == 'cancellation':
        office_number = data['params']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        row = cur.fetchone()

        if not row:
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 99, "message": "Office not found"},
                "id": req_id
            }

        # офис не занят
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

        cur.execute("UPDATE offices SET tenant='' WHERE number=%s", (office_number,))
        conn.commit()
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": req_id
    }
