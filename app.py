from flask import Flask, url_for, request, redirect, abort, render_template 
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
    style = url_for("static", filename="error.css")
    path = url_for("static", filename="error.jpg")
    
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
            'Content-Type': 'text/plain; charset=utf-8' # браузер интерпретирует содержимое как обычный текст
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

# lab-2

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэша'

flower_list = ['роза', 'тюльпан', 'пион', 'гипсофила', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    style = url_for("static", filename="main.css")

    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{style}">
</head>
<body>
    <header>
        WEB-программирование, часть 2. Лабораторная работа 2
    </header>

    <main>
        <div>{"Цветок: " + flower_list[flower_id]}<div>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    <main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 3 курс, 2025
    </footer>
</body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Добавлен цветок: {name} </p>
        <p>Всего цветов: {len(flower_list)} </p>
        <p>Полный список: {flower_list} </p>
    </body>
</html>
'''

@app.route('/lab2/flowers')
def all_flowers():
    style = url_for("static", filename="main.css")
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{style}">
</head>
<body>
    <header>
        WEB-программирование, часть 2. Лабораторная работа 2
    </header>

    <main>
        <h1>Все цветы</h1>
        <p>Общее количество цветов: {len(flower_list)}</p>
        <h2>Список цветов:</h2>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list)}
        </ul>
    <main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 3 курс, 2025
    </footer>
</body>
</html>
'''

@app.route('/lab2/add_flower/')
def not_add_flower():
    style = url_for("static", filename="lab1.css")
    
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{style}">
    <title>Ошибка 400</title>
</head>
<body class="err">
    <div class="err">
        <h1 class="err">Ошибка 400 - Неверный запрос</h1>
        <p class="err">Вы не задали имя цветка</p>
    </div>
</body>
</html>
''', 400

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    style = url_for("static", filename="main.css")
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{style}">
</head>
<body>
    <header>
        WEB-программирование, часть 2. Лабораторная работа 2
    </header>

    <main>
        <h1>Список цветов очищен</h1>
        <p>Все цветы были удалены из списка.</p>
        <p>Текущее количество цветов: {len(flower_list)}</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </main>

    <footer>
        &copy; Федотова Юлия, ФБИ-31, 3 курс, 2025
    </footer>
</body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, lab_number, group, kurs = 'Fedotova Julka', 2, 'ФБИ-31', '3 курс'
    fruits = [
        {'name': 'ананас', 'price': 150},
        {'name': 'яблоки', 'price': 50},
        {'name': 'мандарины', 'price': 200},
        {'name': 'манго', 'price': 250},
        {'name': 'нектарины', 'price': 90},
    ]
    return render_template('example.html', 
                           name=name, lab_number=lab_number, group=group, 
                           kurs=kurs, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Перенаправление на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

# Перенаправление на /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

# Основной обработчик калькулятора
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    
    operations = {
        'sum': a + b,
        'diff': a - b,
        'mult': a * b,
        'div': a / b if b != 0 else 'деление на ноль',
        'pow': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

@app.route('/lab2/books')
def books():
    books_list = [
        {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и узник Азкабана', 'genre': 'Роман', 'pages': 528},
        {'author': 'Мосян Тунсю', 'title': 'Благословение небожителей. Том 5', 'genre': 'Сянься', 'pages': 464},
        {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
        {'author': 'Мосян Тунсю', 'title': 'Благословение небожителей. Том 3', 'genre': 'Сянься', 'pages': 380},
        {'author': 'Стивен Кинг', 'title': 'Зеленая миля', 'genre': 'Роман', 'pages': 448},
        {'author': 'Кристина Старк', 'title': 'Крылья', 'genre': 'Роман', 'pages': 840},
        {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Маргарет Митчелл', 'title': 'Унесенные ветром', 'genre': 'Роман', 'pages': 1088},
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
        {'author': 'Джейн Остен', 'title': 'Гордость и предубеждение', 'genre': 'Роман', 'pages': 350},
        {'author': 'Дэниела Киза', 'title': 'Цветы для Элджернона', 'genre': 'Фантастика, психологическая драма', 'pages': 240}
    ]
    return render_template('books.html', books=books_list)

@app.route('/lab2/iphone')
def iphone_evolution():
    iphone_list = [
        {'title': 'iPhone (2007)', 'image': 'i-2007.png', 'description': 'Первый телефон компании Apple', 'year': 2007},
        {'title': 'iPhone 3G', 'image': 'i-2008.jpg', 'description': 'Второй, почти такой же, телефон компании Apple', 'year': 2008},
        {'title': 'iPhone 3GS', 'image': 'i-2009.jpg', 'description': 'Третий такой же кирпич', 'year': 2009},
        {'title': 'iPhone 4', 'image': 'iphone-4.jpg', 'description': 'Уже что-то новенькое...', 'year': 2010},
        {'title': 'iPhone 4S', 'image': 'iphone-4s.jpg', 'description': 'Снова идентичная новая модель', 'year': 2011},
        {'title': 'iPhone 5', 'image': 'iphone-5.jpg', 'description': 'Пошел тяжелый люкс...', 'year': 2012},
        {'title': 'iPhone 5S и iPhone 5C', 'image': 'iphone-5SC.jpg', 'description': 'Впервые сделали сканер отпечатка пальцев, камеру со Slow-motion и многое другое', 'year': 2013},
        {'title': 'iPhone 6/6 Plus', 'image': 'iphone-6.jpg', 'description': 'iPhone 6 получил более скругленные края, а также, впервые, поддержку NFC', 'year': 2014},
        {'title': 'iPhone 6S/6S Plus', 'image': 'iphone-6s.jpg', 'description': '«Ускоренные» версии появились для обеих «шестерок»', 'year': 2015},
        {'title': 'iPhone 7/7 Plus', 'image': 'iphone-7.webp', 'description': 'Критики начали обвинять Apple в отсутствии инноваций', 'year': 2016},
        {'title': 'iPhone SE', 'image': 'iphone-se.webp', 'description': 'Большая диагональ нравилась не всем, поэтому в Apple попытались повторить успех iPhone 6 и представили iPhone SE', 'year': 2016},
        {'title': 'iPhone 8/8 Plus', 'image': 'iphone-8.jpg', 'description': '«Восьмерка» стала одним из самых слабых продуктов от Apple', 'year': 2017},
        {'title': 'iPhone X', 'image': 'iphone-x.jpg', 'description': 'Начало поколения «бескнопочных» iPhone', 'year': 2017},
        {'title': 'iPhone Xs/Xs Max/ Xr', 'image': 'iphone-xs.jpg', 'description': 'Наибольшей популярностью стал пользоваться iPhone Xr, который благодаря диагонали экрана стал «золотой серединой»', 'year': 2018},
        {'title': 'iPhone 11/11 Pro/11 Pro Max', 'image': 'iphone-11.jpg', 'description': 'АФИГЕТЬ АЙФОН 11 БЫЛ ВЫПУЩЕН В 2019 ГОДУ', 'year': 2019},
        {'title': 'iPhone 12/12 Pro/12 Pro Max/12 Mini, iPhone SE 2 Gen', 'image': 'iphone-12.webp', 'description': 'Слишком много айфонов за раз', 'year': 2020},
        {'title': 'iPhone 13/13 Pro/13 Pro Max/13 Mini', 'image': 'iphone-13.jpg', 'description': 'У меня, кстати, 13 айфон. Мой первый и последний, пока что, айфон))', 'year': 2021},
        {'title': 'iPhone 14/14 Pro/14 Pro Max/14 Plus', 'image': 'iphone-14.jpg', 'description': 'Ну остальные уже одинаковые пошли', 'year': 2022},
        {'title': 'iPhone 15, iPhone 15 Plus, iPhone 15 Pro и iPhone 15 Pro Max', 'image': 'iphone-15.jpg', 'description': 'Ну, я же говорю, одинаковые...', 'year': 2023},
        {'title': 'iPhone 16, iPhone 16 Plus, iPhone 16 Pro и iPhone 16 Pro Max', 'image': 'iphone-16.png', 'description': 'ноу комментс...', 'year': 2024},
        {'title': 'iPhone 17, iPhone 17 Air, iPhone 17 Pro и iPhone 17 Pro Max', 'image': 'iphone-17.jpg', 'description': 'Конец!', 'year': 2025},
    ]
    return render_template('iphone.html', iphones=iphone_list)
