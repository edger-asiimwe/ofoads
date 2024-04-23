from flask import Blueprint

client = Blueprint('client', '__name__')

from . import routes
from . .models import db