from wtforms import form, fields

from flask_admin.contrib.pymongo import ModelView
from flask_admin.model.fields import InlineFormField, InlineFieldList


class MetaInfoForm(form.Form):
    cnt_vote = fields.IntegerField('Vote Count')
    cnt_hit = fields.IntegerField('Hit Count')
    cnt_comment = fields.IntegerField('Comment Count')
    created_at = fields.DateTimeField('Created At')


class PostForm(form.Form):
    site = fields.StringField('Site')
    board = fields.StringField('Board')
    id = fields.IntegerField('Id')

    title = fields.StringField('Title')
    body = fields.TextAreaField('Body')
    created_at = fields.DateTimeField('Created At')

    cnt_vote = fields.IntegerField('Vote Count')
    cnt_hit = fields.IntegerField('Hit Count')
    cnt_comment = fields.IntegerField('Comment Count')

    # Form list
    meta_info = InlineFieldList(InlineFormField(MetaInfoForm))


class PostAdminView(ModelView):
    column_list = ('site', 'board', 'id', 'title', 'created_at',)
    column_sortable_list = ('id', 'title', 'created_at',)

    form = PostForm

    def get_list(self, *args, **kwargs):
        count, data = super(PostAdminView, self).get_list(*args, **kwargs)

        return count, data
