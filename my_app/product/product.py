#from my_app import app
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from sqlalchemy.sql.expression import not_,or_

from flask_login import login_required
from flask_user import roles_required

from my_app import db, app, ALLOWED_EXTENSIONS_FILES
from my_app import rol_admin_need, cache
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app.product.model.product import ProductForm


product = Blueprint('product',__name__)

import time

@product.route('/test2')
@cache.cached(timeout=60)
def test2():
   time.sleep(3)
   return "Hola mundo"

@product.before_request
@login_required
#@rol_admin_need
@roles_required('Admin')
def constructor():
   pass

def allowed_extensions_file(filename):
   return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_FILES

@product.route('/product')
@product.route('/product/<int:page>')
@cache.cached(timeout=60)
def index(page=1):
   return render_template('product/index.html', products=Product.query.paginate(page,5))

@product.route('/show/<int:id>')
def show(id):
   product = Product.query.get_or_404(id)   
   return render_template('product/show.html', product=product)

@product.route('/show2',defaults={'id':28})
@product.route('/show2/<int:id>')
def show2(id):
   product = Product.query.get_or_404(id)   
   return render_template('product/show.html', product=product)

@product.route('/product-delete/<int:id>')
def delete(id):
   product = Product.query.get_or_404(id)   

   db.session.delete(product)
   db.session.commit()
   flash("Producto eliminado con éxito")

   return redirect(url_for('product.index'))

@product.route('/product-create', methods=('GET', 'POST'))
def create():
   form = ProductForm()#meta={'csrf':False}

   categories = [ (c.id, c.name) for c in Category.query.all()]
   form.category_id.choices = categories

   if form.validate_on_submit():
      #crear producto
      p = Product(request.form['name'],request.form['price'],request.form['category_id'])
      db.session.add(p)
      db.session.commit()
      flash("Producto creado con éxito")
      return redirect(url_for('product.create'))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('product/create.html',form=form)


@product.route('/product-update/<int:id>', methods=['GET','POST'])
def update(id):
   product = Product.query.get_or_404(id)   
   form = ProductForm()#meta={'csrf':False}

   app.logger.info("Actualizar producto")

   categories = [ (c.id, c.name) for c in Category.query.all()]
   form.category_id.choices = categories

   if request.method == 'GET':
      form.name.data = product.name
      form.price.data = product.price
      form.category_id.data = product.category_id

   if form.validate_on_submit():
      #actualizar producto
      product.name = form.name.data
      product.price = form.price.data
      product.category_id = form.category_id.data

      if form.file.data:
         file = form.file.data
         if allowed_extensions_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.file = filename

      db.session.add(product)
      db.session.commit()
      flash("Producto actualizado con éxito")
      return redirect(url_for('product.update',id=product.id))

   if form.errors:
      print("__________")
      print(form.errors.items())
      #print(form.name.errors)
      flash(form.errors.items(),'form-error')

   return render_template('product/update.html',product=product, form=form)
   

@product.route('/test')
def test():
   # consultar
   #p = Product.query.limit(2).all()
   #p = Product.query.limit(2).first()
   #p = Product.query.order_by(Product.id.desc()).all()
   #p = Product.query.get({"id":"P1"})
   #p = Product.query.filter_by(name = "P1").first()
   #p = Product.query.filter(Product.id > 1).all()
   #p = Product.query.filter_by(name = "P1", id=2).first()
   #p = Product.query.filter(Product.name.like('%P%')).all()
   #p = Product.query.filter(not_(Product.id > 1)).all()
   #p = Product.query.filter(or_(Product.id > 1, Product.name=="P1")).all()
   #print(p)

   #crear
   #p = Product("P5",60.8)
   #db.session.add(p)
   #db.session.commit()
   #Product.add(p)

   #actualizar
   #p = Product.query.filter_by(name = "P1", id=1).first()
   #p.name = "UP1"
   #db.session.add(p)
   #db.session.commit()

      #eliminar
   p = Product.query.filter_by(id=1).first()
   db.session.delete(p)
   db.session.commit()
   
   return "Flask"

@product.route('/filter/<int:id>')
def filter(id):
   product = PRODUCTS.get(id)
   return render_template('product/filter.html', product=product)


@product.app_template_filter('iva')
def iva_filter(product):
   if product["price"]:
      return product["price"] * .20 + product["price"]
   return "Sin precio"
