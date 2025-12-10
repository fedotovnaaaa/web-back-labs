from flask import Blueprint, render_template, request, session, redirect, current_app
from os import path
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
   if request.method == 'GET':
       return render_template('lab8/register.html')
   
   login_form = request.form.get('login')
