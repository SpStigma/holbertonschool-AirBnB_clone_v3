#!/usr/bin/python3
"""Initialize the Blueprint for the views of the Airbnb clone project's API."""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
