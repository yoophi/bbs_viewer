# -*- coding: utf8
from __future__ import unicode_literals

from flask_admin.contrib.sqla import ModelView

from instashare.database import db
from instashare.extensions import admin
from .models import UserPointInfo, UserDailyPointInfo, \
    UserPointHistory

admin.add_view(ModelView(UserPointInfo, db.session))
admin.add_view(ModelView(UserDailyPointInfo, db.session))
admin.add_view(ModelView(UserPointHistory, db.session))
