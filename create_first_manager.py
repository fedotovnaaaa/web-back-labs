# add_first_manager.py
from werkzeug.security import generate_password_hash
import psycopg2

conn = psycopg2.connect(
    host='127.0.0.1',
    database='julia_fedotova_knowledge_base',
    user='julia_fedotova_knowledge_base',
    password='1234567890'
)
cur = conn.cursor()

login = 'admin'
password = '1234567890'  # ← ваш пароль
full_name = 'Главный Менеджер'
phone = None
role = 'manager'

password_hash = generate_password_hash(password)

cur.execute("""
    INSERT INTO users_rgz (login, password_hash, full_name, phone, role)
    VALUES (%s, %s, %s, %s, %s)
""", (login, password_hash, full_name, phone, role))

conn.commit()
cur.close()
conn.close()

print("Менеджер admin успешно создан!")
