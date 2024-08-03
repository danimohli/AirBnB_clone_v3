#!/usr/bin/python3
"""
create blueprint
"""

from flask import Blueprint

# Create a Blueprint instance for the API views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Check if the Blueprint was successfully created
if app_views is not None:
    # Import all the view modules to register their routes with the Blueprint
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *