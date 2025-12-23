from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # имя пользователя не должно быть пустым
    if not login_form:
        return render_template('lab8/register.html',
                               error='Логин не может быть пустым')
    
    # пароль не должен быть пустым
    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')
    
    # проверка существования
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/')


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = users.query.filter_by(login = login_form).first()

    # имя пользователя не должно быть пустым
    if not login_form:
        return render_template('lab8/login.html',
                               error='Логин не может быть пустым')
    
    # пароль не должен быть пустым
    if not password_form:
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа. Логин или пароль неверны')


@lab8.route('/lab8/logout/')
@login_required # страница будет доступна только авторизованным пользователям
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles, login=current_user.login)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title:
        return render_template('lab8/create.html',
                               error='Заголовок не может быть пустым')
    
    if not article_text:
        return render_template('lab8/create.html',
                               error='Текст статьи не может быть пустым')
    
    if len(title) > 50:
        return render_template('lab8/create.html',
                               error='Заголовок должен быть не длиннее 50 символов')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        return redirect('/lab8/articles/')
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title:
        return render_template('lab8/edit.html',
                               article=article,
                               error='Заголовок не может быть пустым')
    
    if not article_text:
        return render_template('lab8/edit.html',
                               article=article,
                               error='Текст статьи не может быть пустым')
    
    if len(title) > 50:
        return render_template('lab8/edit.html',
                               article=article,
                               error='Заголовок должен быть не длиннее 50 символов')
    
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    
    db.session.commit()
    
    return redirect('/lab8/articles/')


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        return redirect('/lab8/articles/')
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles/')


@lab8.route('/lab8/public_articles', methods=['GET'])
def public_articles():
    articles_list = articles.query.filter_by(is_public=True).all()
    if current_user.is_authenticated:
        return render_template('lab8/public_articles.html', login=current_user.login, articles=articles_list)
    return render_template('lab8/public_articles.html', articles=articles_list)


@lab8.route('/lab8/user_search', methods=['GET'])
@login_required
def search_user_articles():
    # получение поискового запроса из URL-параметров
    query = request.args.get('q')
    user_articles = articles.query.filter(
        # поиск по заголовку
        articles.title.ilike(f'%{query}%'),
        # статьи принадлежат текущему пользователю
        articles.login_id == current_user.id
    ).all() # получаем найденные записи
    return render_template('lab8/search_user_articles.html', user_articles=user_articles, query=query, login=current_user.login)


@lab8.route('/lab8/public_search', methods=['GET'])
def search_public_articles():
    query = request.args.get('q')
    public_articles = articles.query.filter(
        articles.title.ilike(f'%{query}%'),
        articles.is_public == True
    ).all()
    if current_user.is_authenticated:
        return render_template('lab8/search_public_articles.html', public_articles=public_articles, query=query, login=current_user.login)
    return render_template('lab8/search_public_articles.html', public_articles=public_articles, query=query)


@lab8.route('/lab8/favorites')
@login_required
def favorites():
    favorite_articles = articles.query.filter_by(login_id=current_user.id, is_favorite=True).all()
    return render_template('lab8/favorites.html', articles=favorite_articles, login=current_user.login)
