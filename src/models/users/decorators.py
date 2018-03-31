from functools import wraps
from src.app import app
from flask import session, redirect, url_for, request


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['email'] is None or 'email' not in session.keys():
            return redirect(url_for('users.login_user', next = request.path))
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['email'] is None or 'email' not in session.keys():
            return redirect(url_for('users.login_user', next = request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function