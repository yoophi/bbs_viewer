# coding: utf-8
from __future__ import unicode_literals

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from flask.ext.api_app.database import BaseMixin
from instashare.database import db


class UserPointInfo(db.Model, BaseMixin):
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref=backref("point_info", uselist=False))

    total_saved_point = db.Column(db.Integer)
    saved_point = db.Column(db.Integer)
    used_point = db.Column(db.Integer)


class UserDailyPointInfo(db.Model, BaseMixin):
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='daily_point_info')

    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)

    saved_point = db.Column(db.Integer)
    used_point = db.Column(db.Integer)


class UserPointHistory(db.Model, BaseMixin):
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='user_point_histories')

    source_type = db.Column(db.Integer)  # 포인트 적립/소비에 대한 카테고리

    tran_uuid = db.Column(db.Unicode)
    tran_type = db.Column(db.Integer)
    tran_description = db.Column(db.UnicodeText)

    point = db.Column(db.Integer)
    point_change = db.Column(db.Integer)
    point_balance = db.Column(db.Integer)  # 잔여 포인트

    tax = db.Column(db.Integer)


class ShoppingTransaction(db.Model, BaseMixin):
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User')

    product_id = db.Column(db.Integer)
    product_name = db.Column(db.Unicode)
    quantity = db.Column(db.Integer)

    point = db.Column(db.Integer)  # 구입에 사용한 포인트
    result_type = db.Column(db.Integer)
