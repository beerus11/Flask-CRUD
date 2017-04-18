from flask import Flask, redirect, Response, abort, flash, url_for
from flask import render_template
from flask import request
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

# Create app
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

##Constants
product_status_arr = ['Published', 'Not Published', 'Removed', 'Out of Stock']
order_status_arr = ['Pending', 'Approved', 'Received', 'Cancelled']
parent_category_arr = ['Groceries', 'Fashion', 'Electronics']
role_arr = ['Admin', 'Customer']


# Models
class Users(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(1024))
    address = db.Column(db.String(250))
    phone = db.Column(db.String(12))
    role = db.Column(db.Integer)

    def __init__(self, username, email, password, address, phone, role):
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Products(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(120))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)
    status = db.Column(db.String(20))

    def __init__(self, product_name, category, price, date_added, status):
        self.product_name = product_name
        self.category = category
        self.price = price
        self.date_added = date_added
        self.status = status


class Category(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64))
    parent_category = db.Column(db.String(64))

    def __init__(self, category_name, parent_category):
        self.category_name = category_name
        self.parent_category = parent_category


class Orders(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    customer = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))
    status = db.Column(db.String(20))
    address = db.Column(db.String(250))
    price = db.Column(db.Integer)

    def __init__(self, date, customer, product, status, address, price):
        self.date = date
        self.customer = customer
        self.product = product
        self.status = status
        self.address = address
        self.price = price


@app.route('/')
@app.route('/home')
@login_required
def index():
    table = {}
    sum = 0
    for order in Orders.query.all():
        sum += order.price
    table['total_order'] = Orders.query.count()
    table['order_value'] = sum
    table['total_users'] = Users.query.count()
    table['total_products'] = Products.query.count()
    return render_template('index.html', title="Home", user=current_user, data=table)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['password']
    registered_user = Users.query.filter_by(email=email, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('index'))


@app.route('/addUser', methods=['POST'])
def addUser():
    print request.form
    if request.method == 'GET':
        return render_template('register.html')
    user = Users(request.form['username'], request.form['email'],
                 request.form['password'], request.form['address'], request.form['phone'], request.form['role'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/delUser', methods=['POST'])
def delUser():
    print request.form
    print request.args
    if request.method == 'GET':
        return redirect(url_for('users'))
    user = Users.query.filter_by(username=request.form['username']).first()
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted !')
    return redirect(url_for('users'))


@app.route('/editUser', methods=['POST'])
def editUser():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('users'))
    user = Users.query.filter_by(username=request.form['username']).first()
    user.email = request.form['email']
    user.password = request.form['password']
    user.address = request.form['address']
    user.phone = request.form['phone']
    user.role = request.form['role']
    db.session.commit()
    flash('User Edited')
    return redirect(url_for('users'))


@app.route('/addProduct', methods=['POST'])
def addProduct():
    print request.form
    if request.method == 'GET':
        redirect(url_for('products'))
    product = Products(request.form['product_name'], request.form['category'],
                       request.form['price'], datetime.now(), product_status_arr[int(request.form['status'])])
    db.session.add(product)
    db.session.commit()
    flash('Product Added Successfully!')
    return redirect(url_for('products'))


@app.route('/delProduct', methods=['POST'])
def delProduct():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('products'))
    product = Products.query.filter_by(id=int(request.form['id'])).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted !')
    return redirect(url_for('products'))


@app.route('/editProduct', methods=['POST'])
def editProduct():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('products'))
    product = Products.query.filter_by(id=int(request.form['id'])).first()
    print product
    product.product_name = request.form['product_name']
    product.category = request.form['category']
    product.price = request.form['price']
    product.status = product_status_arr[int(request.form['status'])]
    db.session.commit()
    flash('Product Edited')
    return redirect(url_for('products'))


@app.route('/addCategory', methods=['POST'])
def addCategory():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('categories'))
    category = Category(request.form['category_name'], parent_category_arr[int(request.form['parent_category'])])
    db.session.add(category)
    db.session.commit()
    flash('Category Added !')
    return redirect(url_for('categories'))


@app.route('/delCategory', methods=['POST'])
def delCategory():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('categories'))
    category = Category.query.filter_by(category_name=int(request.form['category_name'])).first()
    db.session.delete(category)
    db.session.commit()
    flash('Category Deleted !')
    return redirect(url_for('categories'))


@app.route('/editCategory', methods=['POST'])
def editCategory():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('categories'))
    product = Products.query.filter_by(category_name=int(request.form['category_name'])).first()
    product.parent_category = request.form['parent_category']
    db.session.commit()
    flash('Category Edited')
    return redirect(url_for('categories'))


@app.route('/addOrder', methods=['POST'])
def addOrders():
    print request.args
    print request.form
    if request.method == 'GET':
        return redirect(url_for('orders'))
    order = Orders(datetime.now(), request.form['customer'], request.form['product'],
                   order_status_arr[int(request.form['status'])], request.form['address'], request.form['price'])
    db.session.add(order)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('orders'))


@app.route('/editOrders', methods=['POST'])
def editOrders():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('orders'))
    order = Orders.query.filter_by(id=int(request.form['id'])).first()
    order.customer = request.form['customer']
    order.product = request.form['product']
    order.status = request.form['status']
    order.address = request.form['address']
    order.price = request.form['price']
    db.session.commit()
    flash('Product Edited')
    return redirect(url_for('orders'))


@app.route('/delOrders', methods=['POST'])
def delOrders():
    print request.form
    if request.method == 'GET':
        return redirect(url_for('orders'))
    order = Orders.query.filter_by(id=int(request.form['id'])).first()
    db.session.delete(order)
    db.session.commit()
    flash('Order Deleted !')
    return redirect(url_for('orders'))


@app.route('/products')
@login_required
def products():
    return render_template('products.html', title="Products", user=current_user, data=Products.query.all(),
                           categories=Category.query.all())


@app.route('/users')
@login_required
def users():
    return render_template('users.html', title="Users", user=current_user, data=Users.query.all())


@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html', title="Categories", user=current_user, data=Category.query.all())


@app.route('/orders')
@login_required
def orders():
    customers = Users.query.filter_by(role=2)
    products = Products.query.all()
    return render_template('orders.html', title="Orders", user=current_user, data=Orders.query.all(),
                           customers=customers, products=products)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login", code=302)


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


if __name__ == '__main__':
    app.run()
