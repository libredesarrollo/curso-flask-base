from flask.views import MethodView
from flask import request
from my_app.product.model.product import Product
from my_app.rest_api.helper.request import sendResJson
from my_app import app, db
import json

class ProductApi(MethodView):
    def get(self, id=None):
        products = Product.query.all()

        if id:
            product = Product.query.get(id)
            res = productToJson(product)
        else:
            res = []
            for p in products:
                res.append(productToJson(p))

        return sendResJson(res,None,200)

    def post(self):

        if not request.form:
            return sendResJson(None,"Sin parámetros",403)
        
        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"Sin parámetro nombre",403)
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no válido",403)

        #validaciones precio
        if not "price" in request.form:
            return sendResJson(None,"Sin parámetro precio",403)

        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None,"Precio no válido",403)

        #validaciones category_id
        if not "category_id" in request.form:
            return sendResJson(None,"Sin parámetro categoría",403)

        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None,"Categoría no válida",403)

        #if request.form['price'] is not float:
            #return "Precio no válido",403

        p = Product(request.form['name'],request.form['price'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()

        return sendResJson(productToJson(p),None,200)

    def put(self,id):
        p = Product.query.get(id)   
        if not p:
            return sendResJson(None,"Producto no existe",403)

        if not request.form:
            return sendResJson(None,"Sin parámetros",403)
        
        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"Sin parámetro nombre",403)
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no válido",403)

        #validaciones precio
        if not "price" in request.form:
            return sendResJson(None,"Sin parámetro precio",403)

        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None,"Precio no válido",403)

        #validaciones category_id
        if not "category_id" in request.form:
            return sendResJson(None,"Sin parámetro categoría",403)

        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None,"Categoría no válida",403)

        #if request.form['price'] is not float:
            #return "Precio no válido",403

        p.name = request.form['name']
        p.price = request.form['price']
        p.category_id = request.form['category_id']
        
        db.session.add(p)
        db.session.commit()

        return sendResJson(productToJson(p),None,200)

    def delete(self,id):
        product = Product.query.get(id)   
        if not product:
            return sendResJson(None,"Producto no existe",403)
        
        db.session.delete(product)
        db.session.commit()

        return sendResJson("Producto eliminado",None,200)

def productToJson(product: Product):
    return {
                'id': product.id,
                'name': product.name,
                'category_id':product.category_id,
                'category':product.category.name
            }


product_view = ProductApi.as_view('product_view')
app.add_url_rule('/api/products/',
view_func=product_view,
methods=['GET','POST'])
app.add_url_rule('/api/products/<int:id>',
view_func=product_view,
methods=['GET','DELETE', 'PUT'])




