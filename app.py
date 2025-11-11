import os
from flask import Flask, url_for, request
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


@app.errorhandler(404)
def handle_404(error):
    return not_found()


@app.errorhandler(500)
def handle_500(error):
    return internal_server_error()


access_log = []


@app.route('/404')
def not_found():
    # Логирование доступа
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    log_entry = {
        'ip': client_ip,
        'date': access_date,
        'url': requested_url
    }
    access_log.append(log_entry)
    
    # Генерация путей к статическим файлам
    style = url_for("static", filename="/lab1/error.css")
    path = url_for("static", filename="/lab1/error.jpg")
    
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="''' + style + '''">
    <title>404 Not Found</title>
</head>
<body>
    <div>
        <div class="error-content">
            <div class="error-header">
                <h1>404</h1>
                <h2>Страница не найдена</h2>
            </div>
            
            <div class="error-image">
                <img src="''' + path + '''" alt="404 Error">
            </div>
            
            <div class="error-message">
                <p>Запрашиваемая страница или ресурс не найдены на сервере.</p>
                <p>Скоро фиксики все пофиксят, а пока немного подождите))</p>
                <p>Можете пока вернуться на главную страницу.</p>
            </div>
            
            <div class="error-info">
                <div class="info-item">
                    <strong>Ваш IP-адрес:</strong> ''' + client_ip + '''
                </div>
                <div class="info-item">
                    <strong>Дата доступа:</strong> ''' + access_date + '''
                </div>
                <div class="info-item">
                    <strong>Запрошенный URL:</strong> ''' + requested_url + '''
                </div>
            </div>
            
            <a href="/" class="home-button">Вернуться на главную страницу</a>
        </div>
        
        <div class="log-section">
            <h3>Журнал посещений</h3>
            <p>История всех обращений к несуществующим страницам:</p>
            
            <div class="log-table-container">
                <table class="log-table">
                    <thead>
                        <tr>
                            <th>IP-адрес</th>
                            <th>Дата и время</th>
                            <th>Запрошенный URL</th>
                        </tr>
                    </thead>
                    <tbody>
''' + ''.join(f'''
                        <tr>
                            <td>{entry['ip']}</td>
                            <td>{entry['date']}</td>
                            <td>{entry['url']}</td>
                        </tr>
''' for entry in reversed(access_log)) + '''
                    </tbody>
                </table>
            </div>
            
            <div class="log-footer">
                <p>Всего записей в журнале: ''' + str(len(access_log)) + '''</p>
            </div>
        </div>
    </div>
</body>
</html>
''', 404


@app.route('/500')
def internal_server_error():
    style = url_for("static", filename="/lab1/lab1.css")
    
    return '''
<!doctype html>
<html lang="ru">
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>500 - Ошибка сервера</title>
</head>
<body class="err">
    <h1 class="err">500</h1>
    <p class="err">Внутренняя ошибка сервера</p>
    <p class="err">Произошла непредвиденная ошибка на сервере. Пожалуйста, попробуйте позже.</p>
</body>
</html>
''', 500


@app.route("/")
@app.route("/index")
def index():
    style = url_for("static", filename="/lab1/lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="''' + style + '''">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>

<body>
    <header>
        НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных.
    </header>

    <main>
        <h1>Лабораторные работы по WEB-программированию</h1>
        
        <div class="menu">
            <ul>
                <li>
                    <a href="/lab1">Лабораторная работа 1</a>
                </li>
                <li>
                    <a href="/lab2">Лабораторная работа 2</a>
                </li>
                <li>
                    <a href="/lab3">Лабораторная работа 3</a>
                </li>
                <li>
                    <a href="/lab4">Лабораторная работа 4</a>
                </li>
                <li>
                    <a href="/lab5">Лабораторная работа 5</a>
                </li>
            </ul>
        </div>
    </main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 2 курс, 2025
    </footer>
</body>
</html>
'''

