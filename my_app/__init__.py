from flask import redirect, url_for, Flask, request
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps
#from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_babel import Babel
from flask_user import UserManager
from flask_user.signals import user_registered
from flask_restless import APIManager
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension

#flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os

app = Flask(__name__)


#CSRFProtect(app)
#Bootstrap(app)

ALLOWED_EXTENSIONS_FILES = set(['pdf','jpg','jpeg','gif','png'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/my_app/static/uploads'


#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/pyalmacen"
app.config.from_object('configuration.DevelopmentConfig')
db=SQLAlchemy(app)

from my_app.auth.model.user import Role

#************ flask admin

from my_app.auth.model.user import User,UserModelView
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))

'''from my_app.product.model.product import Product
from my_app.product.model.category import Category

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))'''

#************ fin flask admin
migrate = Migrate(app, db)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en','es'])
    #return "en"

#************ flask User
user_manager = UserManager(app, db, User)




@user_registered.connect_via(app)
def _after_registration_hook(sender, user, **extra):
    rol = Role.query.filter_by(name='Regular').one()
    user.roles.append(rol)
    db.session.add(user)
    db.session.commit()

#************ flask Restless
#restless_manager = APIManager(app,flask_sqlalchemy_db=db)
#restless_manager.create_api(Product, url_prefix='/api/v2',methods=['GET','POST','PATCH','PUT','DELETE'])#

#************ flask Mail
mail = Mail(app)

#************ flask caching
cache = Cache(app)

#************ toolbar debug
#toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "user.login"

def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != "admin":
            logout_user()
            return redirect(url_for('user.login'))#fauth.login
            #login_manager.unauthorized()
            #return "Tu debes ser admin",403
            #print('Calling decorated function ' +str(current_user.rol.value))
        return f(*args, **kwds)
    return wrapper

from my_app.product.product import product
from my_app.product.category import category
from my_app.product.userController import userBp
from my_app.auth.views import auth
from my_app.fauth.views import fauth
from my_app.spavue.views import spavue

#rest
from my_app.rest_api.product_api import product_view
from my_app.rest_api.category_api import category_view

#general
import my_app.general.error_handle

#importar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(userBp)
#app.register_blueprint(auth)
#app.register_blueprint(fauth)
app.register_blueprint(spavue)

#db.create_all()

@app.template_filter('mydouble')
def mydouble_filter(n:float):
    return n*2
