from flask import Blueprint, render_template, request, json, redirect, url_for
from src.models.stores.store import Store
import src.models.users.decorators as User_Decorator

store_bluprint = Blueprint('stores', __name__)

@store_bluprint.route('/store/<string:store_id>')
def store_page(store_id):
    store = Store.get_by_id(store_id)
    return render_template("stores/store.jinja2", store = store)

@store_bluprint.route('/')
def index():
    stores = Store.find_all()
    return  render_template("stores/store_index.jinja2", stores = stores)

@store_bluprint.route('/new', methods=['POST','GET'])
@User_Decorator.admin_required
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag = request.form['tag']
        query = json.loads(request.form['query'])
        store = Store(name, url_prefix,tag,query)
        store.save_to_mongo()
        return redirect(url_for("stores.index"))
    return render_template("stores/create_store.jinja2")

@store_bluprint.route('/edit_store/<string:store_id>', methods = ['POST','GET'])
@User_Decorator.admin_required
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag = request.form['tag']
        query = json.loads(request.form['query'])

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag
        store.query = query

        store.save_to_mongo()
        return redirect(url_for("stores.index"))
    else:
        return render_template("stores/edit_store.jinja2", store = store)

@store_bluprint.route('/delete_store/<string:store_id>')
@User_Decorator.admin_required
def delete_store(store_id):
    store = Store.get_by_id(store_id)
    store.remove()
    return redirect(url_for("stores.index"))
