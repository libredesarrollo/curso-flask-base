from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/pyalmacen"
app.config.from_object('configuration.DevelopmentConfig')
db =SQLAlchemy(app)

from my_app.product.views import product
#importar las vistas
app.register_blueprint(product)

db.create_all()


@app.template_filter('mydouble')
def mydouble_filter(n:float):
    return n*2
