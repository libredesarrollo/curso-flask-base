from flask import Blueprint,session, render_template, request, redirect, url_for, flash, get_flashed_messages
#from werkzeug.exceptions import abort

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db
from flask_login import current_user, login_user, logout_user, login_required
from my_app import login_manager

fauth = Blueprint('fauth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@fauth.route('/register', methods=('GET', 'POST'))
def register():

   print(session)

   #if session.get('username'):
   if 'username' in session:
      print(session['username'])

   form = RegisterForm(meta={'csrf':False})

   if form.validate_on_submit():

      if User.query.filter_by(username=form.username.data).first():
         flash("El usuario ya existe en el sistema",'danger')
      else:
         #crear usuario
         p = User(form.username.data,form.password.data)
         db.session.add(p)
         db.session.commit()
         flash("Usuario creado con éxito")
         return redirect(url_for('auth.register'))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/register.html',form=form)

@fauth.route('/login', methods=('GET', 'POST'))
def login():

   if current_user.is_authenticated:
      flash("Ya estas autenticado")
      return redirect(url_for('product.index'))

   form = LoginForm(meta={'csrf':False})

   if form.validate_on_submit():

      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
         # registrar sesion
         login_user(user)
         flash("Bienvenido de nuevo "+user.username)


         next = request.form['next']
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
         #if not is_safe_url(next):
         #   return .abort(400)
         print(next)

         return redirect(next or url_for('product.index'))
      else:
         flash("Usuario o contraseña incorrectos",'danger')

   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/login.html',form=form)

@fauth.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('fauth.login'))

@fauth.route('/protegido')
@login_required
def protegido():
   return "Vista protegida"