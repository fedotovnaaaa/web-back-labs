from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    if x2 == "0":
        return render_template('lab4/div.html', error_null='На ноль делить нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('/lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


# Вычитание 
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('/lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_trees = 5


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < max_trees:
            tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '111', 'name': 'Алексей Петров', 'gender': 'мужской'},
    {'login': 'bob', 'password': '222', 'name': 'Вася Пупкин', 'gender': 'мужской'},
    {'login': 'ann', 'password': '333', 'name': 'Анна Иоановна', 'gender': 'женский'},
    {'login': 'kate', 'password': '444', 'name': 'Екатерина Петровна', 'gender': 'женский'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            # Находим имя пользователя по логину
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, login=login, name=user_name)
        else:
            authorized = False
            login = ''
            return render_template('lab4/login.html', authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Проверка на пустые значения
    errors = []
    if not login:
        errors.append('не введён логин')
    if not password:
        errors.append('не введён пароль')
    
    # Если есть ошибки валидации
    if errors:
        return render_template('lab4/login.html', errors=errors, login_value=login, authorized=False)
    
    # Проверка логина и пароля
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']  # Сохраняем имя в сессии
            return redirect('/lab4/login')

    # Если логин/пароль неверные
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login_value=login, authorized=False)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')
    message = ''
    snowflakes = 0
    error = ''
    
    if request.method == 'POST':
        if not temperature:
            error = 'Ошибка: не задана температура'
        else:
            try:
                temp = float(temperature)
                if temp < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение'
                elif temp > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temp <= -9:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 3
                elif -8 <= temp <= -5:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 2
                elif -4 <= temp <= -1:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 1
            except ValueError:
                error = 'Ошибка: введите числовое значение температуры'
    
    return render_template('lab4/fridge.html', 
                         message=message, 
                         error=error, 
                         snowflakes=snowflakes,
                         temperature=temperature or '')


# Цены на зерно
grain_prices = {
    'barley': 12000,  # ячмень
    'oats': 8500,     # овёс
    'wheat': 9000,    # пшеница
    'rye': 15000      # рожь
}

grain_names = {
    'barley': 'ячмень',
    'oats': 'овёс', 
    'wheat': 'пшеница',
    'rye': 'рожь'
}


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain_order():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    message = ''
    error = ''
    discount_applied = False
    discount_amount = 0
    total_amount = 0
    final_amount = 0
    
    if request.method == 'POST':
        # Проверка на пустой вес
        if not weight:
            error = 'Ошибка: не указан вес заказа'
        else:
            try:
                weight_float = float(weight)
                
                # Проверка на отрицательный или нулевой вес
                if weight_float <= 0:
                    error = 'Ошибка: вес должен быть положительным числом'
                # Проверка на слишком большой объем
                elif weight_float > 100:
                    error = 'Извините, такого объёма сейчас нет в наличии'
                else:
                    # Проверка выбора зерна
                    if not grain_type:
                        error = 'Ошибка: не выбрано зерно'
                    else:
                        # Расчет стоимости
                        price_per_ton = grain_prices.get(grain_type)
                        grain_name = grain_names.get(grain_type)
                        total_amount = weight_float * price_per_ton
                        
                        # Применение скидки
                        if weight_float > 10:
                            discount_amount = total_amount * 0.1
                            final_amount = total_amount - discount_amount
                            discount_applied = True
                            message = (f'Заказ успешно сформирован. Вы заказали {grain_name}. '
                                     f'Вес: {weight_float} т. Сумма к оплате: {final_amount:,.0f} руб. '
                                     f'Применена скидка 10% за большой объём. Размер скидки: {discount_amount:,.0f} руб.')
                        else:
                            final_amount = total_amount
                            message = (f'Заказ успешно сформирован. Вы заказали {grain_name}. '
                                     f'Вес: {weight_float} т. Сумма к оплате: {final_amount:,.0f} руб.')
                        
            except ValueError:
                error = 'Ошибка: вес должен быть числом'
    
    return render_template('lab4/grain.html',
                         message=message,
                         error=error,
                         grain_type=grain_type or '',
                         weight=weight or '',
                         discount_applied=discount_applied,
                         grain_prices=grain_prices,
                         grain_names=grain_names)

