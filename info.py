from flask import Blueprint, render_template
from functools import wraps

info_routes = Blueprint('my_routes', __name__)

""" @info_routes.route('/manual')
def manual():
    return render_template("manual.html")
#----------------------------------------------------------------------RUTA EJEMPLOS-----------------
@info_routes.route('/ejemplos')
def ejemplos():
    return render_template("ejemplos.html")
#----------------------------------------------------------------------RUTA INFORMACION REBA-----------------
@info_routes.route('/info_reba')
def info_reba():
    return render_template("info_reba.html")
#----------------------------------------------------------------------RUTA INFORMACION RULA-----------------
@info_routes.route('/info_rula')
def info_rula():
    return render_template("info_rula.html") """
#----------------------------------------------------------------------RUTA INFORMACION OCRA-----------------
@info_routes.route('/info_ocra')
def info_ocra():
    return render_template("info_ocra.html")    
