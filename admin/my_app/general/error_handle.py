from sqlalchemy.exc import DataError
from werkzeug.exceptions import HTTPException

from my_app import app
from flask import render_template

#@app.errorhandler(404)
def page_not_found(e):
   return render_template("general/404.html"),404

#@app.errorhandler(Exception)
def error_server(e):
#    print(e.__class__.__name__)
#    print(isinstance(e, DataError))
#    if isinstance(e, DataError):
#        return "Error DataError"

    return render_template("general/500.html",e=e),500
