from flask import Flask, redirect, Response, abort, flash, url_for
from flask import render_template
from flask import request
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# Create app
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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


class Category(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64))
    parent_category = db.Column(db.String(64))


class Orders(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    customer = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))
    status = db.Column(db.String(20))
    address = db.Column(db.String(250))
    price = db.Column(db.Integer)


@app.route('/')
@app.route('/home')
@login_required
def index():
    print current_user
    return render_template('index.html',title="Home",user=current_user)


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


@app.route('/products')
@login_required
def products():
    return render_template('products.html')


@app.route('/users')
@login_required
def users():
    return render_template('users.html')


@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html')


@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html')


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
