from flask import Blueprint,session, render_template, request, redirect, url_for, flash, get_flashed_messages

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=('GET', 'POST'))
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

@auth.route('/login', methods=('GET', 'POST'))
def login():
   form = LoginForm(meta={'csrf':False})

   if form.validate_on_submit():

      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
         # registrar sesion
         session['username'] = user.username
         session['rol'] = user.rol.value
         session['id'] = user.id
         flash("Bienvenido de nuevo "+user.username)
         return redirect(url_for('product.index'))
      else:
         flash("Usuario o contraseña incorrectos",'danger')

   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/login.html',form=form)

@auth.route('/logout')
def logout():
   session.pop('username')
   session.pop('id')
   session.pop('rol')
   return redirect(url_for('auth.login'))