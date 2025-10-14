from flask import Blueprint, url_for, request, redirect, abort, render_template 
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэша'


flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'пион', 'price': 320},
    {'name': 'гипсофила', 'price': 330},
    {'name': 'ромашка', 'price': 300}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    
    flower = flower_list[flower_id]
    return render_template('/lab2/flower_detail.html', 
                         flower_name=flower['name'],
                         flower_price=flower['price'],
                         flower_id=flower_id,
                         total_count=len(flower_list))


@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    # Добавляем цветок с ценой по умолчанию
    flower_list.append({'name': name, 'price': 300})
    return render_template('/lab2/flower_added.html', name=name, price=300, lab_num=2)


@lab2.route('/lab2/add_flower_empty', methods=['GET'])
def add_flower_empty():
    name = request.args.get('name')
    price = request.args.get('price')
    
    if name and price:
        flower_list.append({'name': name, 'price': int(price)})
        return render_template('/lab2/flower_added.html', name=name, price=price, lab_num=2)
    else:
        return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/flowers')
def all_flowers():
    return render_template('/lab2/flowers_list.html', 
                         flower_list=flower_list, 
                         total_count=len(flower_list))


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/add_flower/')
def not_add_flower():
    return "Вы не задали имя цветка", 400


@lab2.route('/lab2/example')
def example():
    name, lab_number, group, kurs = 'Fedotova Julka', 2, 'ФБИ-31', '3 курс'
    fruits = [
        {'name': 'ананас', 'price': 150},
        {'name': 'яблоки', 'price': 50},
        {'name': 'мандарины', 'price': 200},
        {'name': 'манго', 'price': 250},
        {'name': 'нектарины', 'price': 90},
    ]
    return render_template('/lab2/example.html', 
                           name=name, lab_number=lab_number, group=group, 
                           kurs=kurs, fruits=fruits)


@lab2.route('/lab2/')
def lab_2():
    return render_template('/lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('/lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


# Основной обработчик калькулятора
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    
    operations = {
        'sum': a + b,
        'diff': a - b,
        'mult': a * b,
        'div': a / b if b != 0 else 'деление на ноль',
        'pow': a ** b
    }
    return render_template('/lab2/calc.html', a=a, b=b, operations=operations)


@lab2.route('/lab2/books')
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
    return render_template('/lab2/books.html', books=books_list)


@lab2.route('/lab2/iphone')
def iphone_evolution():
    iphone_list = [
        {'title': 'iPhone (2007)', 'image': 'i-2007.png', 'description': 'Первый телефон компании lab2le', 'year': 2007},
        {'title': 'iPhone 3G', 'image': 'i-2008.jpg', 'description': 'Второй, почти такой же, телефон компании lab2le', 'year': 2008},
        {'title': 'iPhone 3GS', 'image': 'i-2009.jpg', 'description': 'Третий такой же кирпич', 'year': 2009},
        {'title': 'iPhone 4', 'image': 'iphone-4.jpg', 'description': 'Уже что-то новенькое...', 'year': 2010},
        {'title': 'iPhone 4S', 'image': 'iphone-4s.jpg', 'description': 'Снова идентичная новая модель', 'year': 2011},
        {'title': 'iPhone 5', 'image': 'iphone-5.jpg', 'description': 'Пошел тяжелый люкс...', 'year': 2012},
        {'title': 'iPhone 5S и iPhone 5C', 'image': 'iphone-5SC.jpg', 'description': 'Впервые сделали сканер отпечатка пальцев, камеру со Slow-motion и многое другое', 'year': 2013},
        {'title': 'iPhone 6/6 Plus', 'image': 'iphone-6.jpg', 'description': 'iPhone 6 получил более скругленные края, а также, впервые, поддержку NFC', 'year': 2014},
        {'title': 'iPhone 6S/6S Plus', 'image': 'iphone-6s.jpg', 'description': '«Ускоренные» версии появились для обеих «шестерок»', 'year': 2015},
        {'title': 'iPhone 7/7 Plus', 'image': 'iphone-7.webp', 'description': 'Критики начали обвинять lab2le в отсутствии инноваций', 'year': 2016},
        {'title': 'iPhone SE', 'image': 'iphone-se.webp', 'description': 'Большая диагональ нравилась не всем, поэтому в lab2le попытались повторить успех iPhone 6 и представили iPhone SE', 'year': 2016},
        {'title': 'iPhone 8/8 Plus', 'image': 'iphone-8.jpg', 'description': '«Восьмерка» стала одним из самых слабых продуктов от lab2le', 'year': 2017},
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
    return render_template('/lab2/iphone.html', iphones=iphone_list)
