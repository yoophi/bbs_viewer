import datetime

import mongoengine
from bson import ObjectId
from flask import flash

from bbs_viewer.database import mongodb as db
from bbs_viewer.extensions import admin
from flask.ext.admin.babel import gettext
from flask.ext.admin.contrib.mongoengine.helpers import format_error
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import rules


class MetaInfo(db.EmbeddedDocument):
    cnt_vote = db.IntField()
    cnt_hit = db.IntField()
    cnt_comment = db.IntField()
    created_at = db.DateTimeField(default=datetime.datetime.now)


class Post(db.Document):
    _id = db.ObjectIdField()

    id = db.IntField()
    title = db.StringField(max_length=255, required=True)
    body = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now)

    site = db.StringField()
    board = db.StringField()

    cnt_vote = db.IntField()
    cnt_hit = db.IntField()
    cnt_comment = db.IntField()

    meta_info = db.ListField(db.EmbeddedDocumentField(MetaInfo))

    meta = {'collection': 'scrapy_items'}


class PostView(ModelView):
    # object_id_converter = str

    form_subdocuments = {
        'meta_info': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('cnt_vote', 'cnt_comment', 'cnt_hit', 'created_at', rules.HTML('<hr>')),
                    'form_widget_args': {
                    }
                }
            }
        }
    }

    def get_pk_value(self, model):
        return model._id


    def scaffold_pk(self):
        return '_id'

    def get_one(self, id):
        """
            Return a single model instance by its ID

            :param id:
                Model ID
        """
        print 'get_one', id
        print 'id', id
        try:
            print self.get_query().filter(_id=ObjectId(id)).first()
            return self.get_query().filter(_id=ObjectId(id)).first()
            # return self.get_query().filter(pk=id).first()
        except mongoengine.ValidationError as ex:
            flash(gettext('Failed to get model. %(error)s',
                          error=format_error(ex)),
                  'error')
            return None


# Add views
admin.add_view(PostView(Post))
