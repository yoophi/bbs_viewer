# coding: utf-8
from __future__ import unicode_literals

from wtforms import Form, StringField, TextAreaField, DateTimeField, \
    SelectField, IntegerField, BooleanField
from wtforms.validators import Length, DataRequired

from instashare.constants import GOAL_TYPE


class CampaignForm(Form):
    """Render HTML input for Appointment model & validate submissions.
    This matches the models.Appointment class very closely. Where
    models.Appointment represents the domain and its persistence, this class
    represents how to display a form in HTML & accept/reject the results.
    """
    name = StringField('이름', [Length(max=255), DataRequired()])
    desc = TextAreaField('설명')
    start_at = DateTimeField('시작 일시')
    end_at = DateTimeField('종료 일시')


class CampaignGoalForm(Form):
    """Render HTML input for Appointment model & validate submissions.
    This matches the models.Appointment class very closely. Where
    models.Appointment represents the domain and its persistence, this class
    represents how to display a form in HTML & accept/reject the results.
    """

    type = SelectField('유형', coerce=int, choices=[
        (GOAL_TYPE.IG_FOLLOW, '인스타그램 팔로우'),
        (GOAL_TYPE.IG_HASHTAG, '인스타그램 해시태그 글쓰기'),
        (GOAL_TYPE.IG_LIKE, '인스타그램 좋아요'),
        (GOAL_TYPE.IG_REGRAM, '인스타그램 리그램'),
        (GOAL_TYPE.IG_SHARE, '인스타그램 공유하기'),
    ])

    point = IntegerField('포인트', validators=[DataRequired()])
    desc = TextAreaField('설명')
    is_public = BooleanField('공개 여부')

    account = StringField('계정')
    url = StringField('게시물 주소')
    hashtag = StringField('해시태그')
    media_id = StringField('미디어ID')
    raw_json = TextAreaField('JSON')
