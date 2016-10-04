from sqlalchemy.orm import relationship
from instashare.database import db


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', backref='connections')

    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    email = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)

    def __repr__(self):
        return '<{self.__class__.__name__}:{self.provider_id}>'.format(self=self)
