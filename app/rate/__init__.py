from flask import Blueprint

rate = Blueprint('rate', __name__)

from .views import *
from .models import *