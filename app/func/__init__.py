from flask import Blueprint

func = Blueprint('func', __name__)

from . import views