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


@lab3.route('/lab3/ticket')
def ticket():
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    errors = {}
    
    # Проверка на пустые поля
    if any([fio, shelf, linen, baggage, age, departure, destination, date, insurance]):
        if not fio:
            errors['fio'] = 'Заполните поле!'
        if not shelf:
            errors['shelf'] = 'Заполните поле!'
        if not linen:
            errors['linen'] = 'Заполните поле!'
        if not baggage:
            errors['baggage'] = 'Заполните поле!'
        if not age:
            errors['age'] = 'Заполните поле!'
        elif not age.isdigit() or int(age) < 1 or int(age) > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
        if not departure:
            errors['departure'] = 'Заполните поле!'
        if not destination:
            errors['destination'] = 'Заполните поле!'
        if not date:
            errors['date'] = 'Заполните поле!'
        if not insurance:
            errors['insurance'] = 'Заполните поле!'
    
    # Если есть ошибки или форма не заполнена, показываем форму
    if errors or not any([fio, shelf, linen, baggage, age, departure, destination, date, insurance]):
        return render_template('lab3/ticket.html', 
                             fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                             age=age, departure=departure, destination=destination,
                             date=date, insurance=insurance, errors=errors)
    
    # Если все поля заполнены корректно, показываем результат
    # Расчет стоимости билета
    if int(age) < 18:
        base_price = 700
        ticket_type = 'Детский билет'
    else:
        base_price = 1000
        ticket_type = 'Взрослый билет'
    
    total_price = base_price
    
    # Доплаты
    if shelf in ['lower', 'lower-side']:
        total_price += 100
    if linen == 'yes':
        total_price += 75
    if baggage == 'yes':
        total_price += 250
    if insurance == 'yes':
        total_price += 150
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, ticket_type=ticket_type,
                         total_price=total_price)


@lab3.route('/lab3/ticket_result')
def ticket_result():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    # Проверка на пустые поля
    if not fio:
        errors['fio'] = 'Заполните поле!'
    if not shelf:
        errors['shelf'] = 'Заполните поле!'
    if not linen:
        errors['linen'] = 'Заполните поле!'
    if not baggage:
        errors['baggage'] = 'Заполните поле!'
    if not age:
        errors['age'] = 'Заполните поле!'
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
    if not departure:
        errors['departure'] = 'Заполните поле!'
    if not destination:
        errors['destination'] = 'Заполните поле!'
    if not date:
        errors['date'] = 'Заполните поле!'
    if not insurance:
        errors['insurance'] = 'Заполните поле!'
    
    # Если есть ошибки, показываем форму снова
    if errors:
        return render_template('lab3/ticket.html', 
                             fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                             age=age, departure=departure, destination=destination,
                             date=date, insurance=insurance, errors=errors)
    
    # Расчет стоимости билета
    if int(age) < 18:
        base_price = 700
        ticket_type = 'Детский билет'
    else:
        base_price = 1000
        ticket_type = 'Взрослый билет'
    
    total_price = base_price
    
    # Доплаты
    if shelf in ['lower', 'lower-side']:
        total_price += 100
    if linen == 'yes':
        total_price += 75
    if baggage == 'yes':
        total_price += 250
    if insurance == 'yes':
        total_price += 150
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, ticket_type=ticket_type,
                         total_price=total_price)


@lab3.route('/lab3/settings_clear')
def settings_clear():
    resp = make_response(redirect('/lab3/settings'))
    # Очищаем все cookies стилей
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('backgroundcolor', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('line_height', '', expires=0)
    resp.set_cookie('text_decoration', '', expires=0)
    return resp
