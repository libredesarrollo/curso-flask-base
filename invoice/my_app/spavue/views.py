from flask import Blueprint, render_template

spavue = Blueprint('spavue',__name__)

@spavue.route('/')
def base():
   return render_template('spavue/base.html')