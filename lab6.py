from flask import Blueprint, render_template, request, session, redirect, current_app


lab6 = Blueprint('lab6', __name__)


offices = []
for i in range(1, 11):
    floor = (i - 1) // 3 + 1  # 3 офиса на этаже
    offices.append({"number": i, "tenant": "", "price": 800 + floor * 200})


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        login = session.get('login')
        if login:
            # Для авторизованного пользователя возвращаем только свободные офисы и его офисы
            user_offices = []
            for office in offices:
                if office['tenant'] == '' or office['tenant'] == login:
                    user_offices.append(office)
            return {
                'jsonrpc': '2.0',
                'result': user_offices,
                'id': id
            }
        else:
            # Для неавторизованного пользователя возвращаем все офисы
            return {
                'jsonrpc': '2.0',
                'result': offices,
                'id': id
            }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
            'code': 1,
            'message': 'Unauthorized'
        },
        'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                # Проверка: офис арендован
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not rented'
                        },
                        'id': id
                    }
    
                # Проверка: офис арендован именно тем пользователем, что сейчас авторизован
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel someone else\'s rental'
                        },
                        'id': id
                    }
                
                # Снимаем аренду
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
                
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
