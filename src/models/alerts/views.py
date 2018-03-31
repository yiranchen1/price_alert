from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as UserDecorators

alert_blueprint = Blueprint('alerts', __name__)

@UserDecorators.login_required
@alert_blueprint.route('/new', methods = ['POST', 'GET'])
def create_alert():
    if request.method == 'POST':
        name = request.form['alert_name']
        url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        item = Item(name, url)
        item.save_to_mongo()
        alert = Alert(session['email'], price_limit,item._id)
        alert.save_to_mongo()
    return render_template("alerts/new_alert.jinja2")

@UserDecorators.login_required
@alert_blueprint.route('/edit/<string:alert_id>', methods = ['POST', 'GET'])
def edit_alert(alert_id):
    alert = Alert.get_by_alert_id(alert_id)
    if request.method == 'POST':
        price = float(request.form['price_limit'])
        alert.price_limit = price
        alert.save_to_mongo()
        return redirect(url_for('users.user_alerts'))
    else:
        return render_template("alerts/edit_alert.jinja2",alert = alert)


@UserDecorators.login_required
@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    Alert.get_by_alert_id(alert_id).deactivate_alert()
    return redirect(url_for('users.user_alerts'))

@UserDecorators.login_required
@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    Alert.get_by_alert_id(alert_id).activate_alert()
    return redirect(url_for('users.user_alerts'))

@UserDecorators.login_required
@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.get_by_alert_id(alert_id).delete_alert()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/<string:alert_id>')
@UserDecorators.login_required
def get_alert_page(alert_id):
    alert = Alert.get_by_alert_id(alert_id)
    return render_template("alerts/alert.jinja2", alert = alert)

@alert_blueprint.route('check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.get_by_alert_id(alert_id).load_item_price()
    return redirect(url_for('alerts.get_alert_page', alert_id = alert_id))


