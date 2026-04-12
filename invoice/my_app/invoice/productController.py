import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages

from my_app.product.model.product import Product

from flask_login import login_required
from flask_security import roles_required
from flask import jsonify, send_file

from my_app.invoice.models import Sell, SellProduct, InvoiceForm
from my_app import db

import pdfkit

invoiceProductBp = Blueprint('invoice_product',__name__)

@invoiceProductBp.before_request
def constructor():
   pass

@invoiceProductBp.route('/invoice/detail/<int:id>')
def detail(id): 
   #pdfkit.from_url('http://google.com', 'out.pdf')
   sell = Sell.query.get_or_404(id)
   return render_template('invoice/detail.html',sell=sell)

@login_required
@roles_required('Regular')
@invoiceProductBp.route('/invoice/detail_pdf/<int:id>')
def detail_pdf(id): 
   
   sell = Sell.query.get_or_404(id)

   path_file = 'static/pdf/factura_{0}.pdf'.format(id)

   pdfkit.from_url('http://127.0.0.1:5000/invoice/detail/{0}'.format(id), 'my_app/'+path_file)
   return send_file(path_file, as_attachment=True)

@login_required
@roles_required('Regular')
@invoiceProductBp.route('/invoice')
@invoiceProductBp.route('/invoice/<int:page>')
def index(page=1):
   sales = Sell.query.paginate(page,10)
   return render_template('invoice/index.html',sales=sales)

@login_required
@roles_required('Regular')
@invoiceProductBp.route('/invoice/dispatch')
def dispatch():

   products = []
   if request.values:
      productSearch = request.values['search']
      products = Product.query.filter(Product.name.like('%{0}%'.format(productSearch))).all()
      print(products)


   return render_template('invoice/dispatch.html',products=products)

@invoiceProductBp.route('/invoice/jsearch_product')
def jsearch_product():

   products = []
   if request.values:
      productSearch = request.values['search']
      products = Product.query.filter(Product.name.like('%{0}%'.format(productSearch))).all()
      print(products)

   return jsonify([ p.serialize for p in products ])

@login_required
@roles_required('Regular')
@invoiceProductBp.route('/invoice/jsell', methods=['POST'])
def jsell():

   if request.method == 'POST':
      form = InvoiceForm()#meta={'csrf':False}
      form.validate_on_submit()
      if form.errors:
         return jsonify({
                           'msj': form.errors,
                           'code': 500
                        })

      sell = Sell()

      sell.name = request.form['name']
      sell.surname = request.form['surname']
      sell.company = request.form['company']

      products = request.form['products'].split(',')

      for p in products:
         product = Product.query.get(p)

         if product is None:
            return jsonify({
                  'msj': "El producto con #{0} no existe".format(p),
                  'code': 501
               })
            #print("Producto no exite")

         sellProduct = SellProduct()
         sellProduct.product_id = product.id
         sell.sellproducts.append(sellProduct)

      db.session.add(sell)
      db.session.commit()

      return jsonify({
                        'msj': "Guardado compra #{0}".format(sell.id),
                        'code':200
                     })

   

