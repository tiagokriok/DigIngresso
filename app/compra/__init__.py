from flask import Blueprint

compra = Blueprint('compra', __name__)

from . import views