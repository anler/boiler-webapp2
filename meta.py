import os

from google.appengine.api import app_identity

from .extensions.static import static

DEBUG = os.getenv('DEBUG', False)

get_application_id = app_identity.get_application_id

templates_path = ('templates',)
template_extensions = (static(static_path='static'),)
