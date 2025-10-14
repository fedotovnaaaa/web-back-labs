from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Julka', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'pink')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}  # Объединяем все ошибки в один словарь
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    # Проверка имени
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    # Проверка возраста
    if age == '':
        errors['age'] = 'Заполните поле!'
    
    return render_template('lab3/form1.html', 
                         user=user, age=age, sex=sex, 
                         errors=errors)  # Передаем один словарь с ошибками


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    backgroundcolor = request.args.get('backgroundcolor')
    font_size = request.args.get('font_size')
    line_height = request.args.get('line_height')
    text_decoration = request.args.get('text_decoration')

    resp = make_response(redirect('/lab3/settings'))
    
    if color:
        resp.set_cookie('color', color)
    
    if backgroundcolor:
        resp.set_cookie('backgroundcolor', backgroundcolor)
    
    if font_size:
        resp.set_cookie('font_size', font_size)
    
    if line_height:
        resp.set_cookie('line_height', line_height)
    
    if text_decoration:
        resp.set_cookie('text_decoration', text_decoration)
    
    # Если нет новых значений, просто рендерим страницу
    if not color and not backgroundcolor and not font_size and not line_height and not text_decoration:
        color = request.cookies.get('color')
        backgroundcolor = request.cookies.get('backgroundcolor')
        font_size = request.cookies.get('font_size')
        line_height = request.cookies.get('line_height')
        text_decoration = request.cookies.get('text_decoration')
        resp = make_response(render_template('lab3/settings.html', 
                                           color=color, 
                                           backgroundcolor=backgroundcolor,
                                           font_size=font_size,
                                           line_height=line_height,
                                           text_decoration=text_decoration))
    
    return resp
