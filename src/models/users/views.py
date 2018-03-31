#blueprint
#endpoint of api that is related to the users
from flask import Blueprint, request, redirect, url_for, render_template, session
import src.models.users.erros as UserErrors
import src.models.users.decorators as UserDecorators


from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods = ['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.massage
    return render_template("users/login.jinja2")


@user_blueprint.route('/register',methods = ['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.massage
    return render_template("users/register.jinja2")

@user_blueprint.route('/alerts')
@UserDecorators.login_required
def user_alerts():
    user = User.get_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template("users/alerts.jinja2", alerts = alerts)

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass

