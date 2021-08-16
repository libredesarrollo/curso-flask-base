#from my_app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.exceptions import abort
from sqlalchemy.sql.expression import not_,or_
from flask_login import login_required

from my_app import db, rol_admin_need
from my_app.product.model.category import Category
from my_app.product.model.category import CategoryForm


category = Blueprint('category',__name__)

@category.before_request
@login_required
@rol_admin_need
def constructor():
   pass


@category.route('/category')
@category.route('/category/<int:page>')
def index(page=1):
   return render_template('category/index.html', categories=Category.query.paginate(page,5))

@category.route('/category/<int:id>')
def show(id):
   category = Category.query.get_or_404(id)   
   return render_template('category/show.html', category=category)

@category.route('/category-delete/<int:id>')
def delete(id):
   category = Category.query.get_or_404(id)   

   db.session.delete(category)
   db.session.commit()
   flash("Categoria eliminado con éxito")

   return redirect(url_for('category.index'))

@category.route('/category-create', methods=('GET', 'POST'))
def create():
   form = CategoryForm(meta={'csrf':False})
   if form.validate_on_submit():
      #crear categoryo
      p = Category(request.form['name'])
      db.session.add(p)
      db.session.commit()
      flash("Categoria creado con éxito")
      return redirect(url_for('category.create'))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('category/create.html',form=form)


@category.route('/category-update/<int:id>', methods=['GET','POST'])
def update(id):
   category = Category.query.get_or_404(id)   
   form = CategoryForm(meta={'csrf':False})

   print(category.products)#.first()

   if request.method == 'GET':
      form.name.data = category.name

   if form.validate_on_submit():
      #actualizar categoryo
      category.name = form.name.data

      db.session.add(category)
      db.session.commit()
      flash("Categoria actualizado con éxito")
      return redirect(url_for('category.update',id=category.id))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('category/update.html',category=category, form=form)
   

@category.route('/test')
def test():
   # consultar
   #p = Category.query.limit(2).all()
   #p = Category.query.limit(2).first()
   #p = Category.query.order_by(Category.id.desc()).all()
   #p = Category.query.get({"id":"P1"})
   #p = Category.query.filter_by(name = "P1").first()
   #p = Category.query.filter(Category.id > 1).all()
   #p = Category.query.filter_by(name = "P1", id=2).first()
   #p = Category.query.filter(Category.name.like('%P%')).all()
   #p = Category.query.filter(not_(Category.id > 1)).all()
   #p = Category.query.filter(or_(Category.id > 1, Category.name=="P1")).all()
   #print(p)

   #crear
   #p = Category("P5",60.8)
   #db.session.add(p)
   #db.session.commit()
   #Category.add(p)

   #actualizar
   #p = Category.query.filter_by(name = "P1", id=1).first()
   #p.name = "UP1"
   #db.session.add(p)
   #db.session.commit()

      #eliminar
   p = Category.query.filter_by(id=1).first()
   db.session.delete(p)
   db.session.commit()
   
   return "Flask"

@category.route('/filter/<int:id>')
def filter(id):
   category = PRODUCTS.get(id)
   return render_template('category/filter.html', category=category)


@category.app_template_filter('iva')
def iva_filter(category):
   if category["price"]:
      return category["price"] * .20 + category["price"]
   return "Sin precio"
