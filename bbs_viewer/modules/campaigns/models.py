import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flask_api_app.database import BaseMixin
from instashare.database import db


class Campaign(db.Model, BaseMixin):
    name = db.Column(db.Unicode(255))

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='campaigns')

    start_at = db.Column(db.DateTime())
    end_at = db.Column(db.DateTime())
    desc = db.Column(db.UnicodeText)

    is_draft = db.Column(db.Boolean)

    @property
    def point(self):
        val = 0
        for item in self.goals:
            val += item.point

        return val


class CampaignGoal(db.Model, BaseMixin):
    campaign = relationship('Campaign', backref='goals')
    campaign_id = db.Column(db.Integer, ForeignKey(Campaign.id), nullable=False)
    type = db.Column(db.Integer())

    point = db.Column(db.Integer)
    desc = db.Column(db.Unicode)

    account = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    media_id = db.Column(db.Unicode)
    hashtag = db.Column(db.Unicode)
    raw_json = db.Column(db.UnicodeText)

    is_public = db.Column(db.Boolean)

    def __repr__(self):
        return '<{self.__class__.__name__}:{self.id}>'.format(self=self)

    @property
    def json(self):
        if self.raw_json:
            return json.loads(self.raw_json)

        return {}

    @property
    def caption(self):
        try:
            return self.json['caption']['text']
        except Exception as e:
            return ''

    @property
    def image_url(self):
        try:
            return self.json['images']['standard_resolution']['url']
        except Exception as e:
            return ''
