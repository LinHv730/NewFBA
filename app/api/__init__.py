from flask import Blueprint

irobotbox = Blueprint('irobotbox',__name__)

from .models.m_irobotbox import *
from .views.v_irobotbox import *