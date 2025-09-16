from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.errorhandler(404)
def handle_404(error):
    return not_found()

@app.errorhandler(400)
def handle_400(error):
    return bad_request()

@app.errorhandler(401)
def handle_401(error):
    return unauthorized()

@app.errorhandler(403)
def handle_403(error):
    return forbidden()

@app.errorhandler(405)
def handle_405(error):
    return method_not_allowed()

@app.errorhandler(418)
def handle_418(error):
    return teapot()

@app.errorhandler(500)
def handle_500(error):
    return internal_server_error()

@app.route('/400')
def bad_request():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>400 Bad Request</title>
</head>
<body class="err">
    <h1 class="err">400 Bad Request</h1>
    <p class="err">Сервер не может обработать запрос из-за некорректного синтаксиса.</p>
    <p class="err">Пожалуйста, проверьте правильность вашего запроса.</p>
</body>
</html>
''', 400

@app.route('/401')
def unauthorized():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>401 Unauthorized</title>
</head>
<body class="err">
    <h1 class="err">401 Unauthorized</h1>
    <p class="err">Требуется аутентификация для доступа к данному ресурсу.</p>
    <p class="err">Пожалуйста, предоставьте корректные учетные данные.</p>
</body>
</html>
''', 401

@app.route('/402')
def payment_required():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>402 Payment Required</title>
</head>
<body class="err">
    <h1 class="err">402 Payment Required</h1>
    <p class="err">Для доступа к данному ресурсу требуется оплата.</p>
    <p class="err">Этот код зарезервирован для будущего использования.</p>
</body>
</html>
''', 402

@app.route('/403')
def forbidden():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>403 Forbidden</title>
</head>
<body class="err">
    <h1 class="err">403 Forbidden</h1>
    <p class="err">Доступ к запрошенному ресурсу запрещен.</p>
    <p class="err">У вас нет необходимых прав для просмотра этой страницы.</p>
</body>
</html>
''', 403

@app.route('/404')
def not_found():
    path = url_for("static", filename="error.jpg")
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>404 Not Found</title>
</head>
<body class="err">
    <h1 class="err">404 Not Found</h1>
    <p class="err">Страницы не существует</p>
    <p class="err">Запрашиваемая страница или ресурс не найдены на сервере.</p>
    <img src="''' + path + '''">
</body>
</html>
''', 404

@app.route('/405')
def method_not_allowed():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>405 Method Not Allowed</title>
</head>
<body class="err">
    <h1 class="err">405 Method Not Allowed</h1>
    <p class="err">Метод запроса не поддерживается для данного ресурса.</p>
    <p class="err">Пожалуйста, используйте допустимый HTTP-метод.</p>
</body>
</html>
''', 405

@app.route('/418')
def teapot():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="''' + style + '''">
    <title>418 I'm a teapot</title>
</head>
<body class="err">
    <h1 class="err">418 I'm a teapot</h1>
    <p class="err">Я - чайник и не могу заваривать кофе.</p>
    <p class="err">Это шуточный код ошибки из RFC 2324 (Hyper Text Coffee Pot Control Protocol).</p>
</body>
</html>
''', 418

@app.route('/500')
def internal_server_error():
    style = url_for("static", filename="lab1.css")
    
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

@app.route("/lab1/error")
def cause_error():
    result = 50 / 0
    return "Этот код никогда не выполнится"

@app.route("/")
@app.route("/index")
def index():
    style = url_for("static", filename="lab1.css")

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
            </ul>
        </div>
    </main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 2 курс, 2025
    </footer>
</body>
</html>
'''

@app.route("/lab1")
def lab_1():
    style = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="''' + style + '''">
    <title>Лабораторная 1</title>
</head>

<body>
    <header>
        НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных.
    </header>

    <main>        
        <div>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.
        </div>
        <p><a href="/">Вернуться на главную</a></p>
    </main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 2 курс, 2025
    </footer>
</body>
</html>
'''


@app.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Федотова Юлия Сергеевна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    style = url_for("static", filename="lab1.css")
    
    html_content = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + style + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''
    return html_content, 200, {
        'Content-Language': 'ru-RU',  # Язык контента - русский
        'X-Custom-Header': 'OAK TREE',  # Пользовательский заголовок 1
        'X-Image-Type': 'Nature',  # Пользовательский заголовок 2
        'X-Author-Name': 'Julka'  # Пользовательский заголовок 3
    }


count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip +'''
    </body>
</html>
'''

@app.route('/lab1/counter/clean')
def clean_counter():
    global count
    count = 0

    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик очищен!</h1>
        <p>Счётчик посещений обнулился((((</p>
        <a href="''' + url_for('counter') + '''">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201
