from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/')
def lab():
    return render_template('lab9/index.html')

