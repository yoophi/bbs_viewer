from flask import jsonify
from marshmallow.fields import Nested

from bbs_viewer.database import mongo
from bbs_viewer.extensions import ma
from flask.ext.api_app.core.api import api


class MetaInfoSchema(ma.Schema):
    class Meta:
        fields = (
            'cnt_comment', 'cnt_hit', 'cnt_vote',
            'created_at',
        )


class PostSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'title', 'body', 'created_at',
            'site', 'board',
            'meta_info',
            'cnt_comment', 'cnt_hit', 'cnt_vote',
        )

    meta_info = Nested(MetaInfoSchema, many=True)


@api.route('/posts')
def posts():
    schema = PostSchema(many=True, exclude=('body',))
    data = mongo.db.scrapy_items.find().limit(10)
    return jsonify(schema.dump(data).data)
