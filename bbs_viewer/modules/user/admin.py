from flask_admin.contrib import sqla

from instashare.database import db
from instashare.extensions import admin
from .models import Connection

admin.add_view(sqla.ModelView(Connection, db.session))