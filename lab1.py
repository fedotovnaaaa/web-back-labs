from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/error")
def cause_error():
    result = 50 / 0
    return "Этот код никогда не выполнится"


@lab1.route("/lab1")
def lab():
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

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1">/lab1</a> - Ссылка на текущую страницу</li>
            <li><a href="/">/</a> - Ссылка на главную страницу</li>
            <li><a href="/index">/index</a> - Ссылка на главную страницу 2.0</li>
            <li><a href="/lab1/web">/lab1/web</a> - Веб-сервер на Flask</li>
            <li><a href="/lab1/author">/lab1/author</a> - Информация об авторе</li>
            <li><a href="/lab1/image">/lab1/image</a> - Дуб</li>
            <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
            <li><a href="/lab1/counter/clean">/lab1/counter/clean</a> - Очистка счетчика</li>
            <li><a href="/lab1/info">/lab1/info</a> - Перенаправление на автора</li>
            <li><a href="/lab1/created">/lab1/created</a> - Страница создания чего-то... (201)</li>
            <li><a href="/lab1/error">/lab1/error</a> - Вызов ошибки сервера (500)</li>
            <li><a href="/400">/400</a> - Ошибка 400. Bad Request</li>
            <li><a href="/401">/401</a> - Ошибка 401. Unauthorized</li>
            <li><a href="/402">/402</a> - Ошибка 402. Payment Required</li>
            <li><a href="/403">/403</a> - Ошибка 403. Forbidden</li>
            <li><a href="/404">/404</a> - Ошибка 404. Not Found</li>
            <li><a href="/405">/405</a> - Ошибка 405. Method Not Allowed</li>
            <li><a href="/418">/418</a> - Ошибка 418. I'm a teapot</li>
            <li><a href="/500">/500</a> - Ошибка 500. Ошибка сервера</li>
        </ul>
    </main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 2 курс, 2025
    </footer>
</body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8' # браузер интерпретирует содержимое как обычный текст
        }


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/image")
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


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/counter/clean')
def clean_counter():
    global count
    count = 0

    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик очищен!</h1>
        <p>Счётчик посещений обнулился((((</p>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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
