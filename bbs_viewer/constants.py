# -*- coding: utf-8 -*-
"""
Constant 정의
"""
from __future__ import unicode_literals

from bbs_viewer.core import main


class EnumConstantMeta(type):
    @staticmethod
    def __new__(cls, name, bases, dct):
        dct['reverse_mapping'] = {
            value: key
            for key, value in dct.iteritems() if not key.startswith('__')
            }

        return super(EnumConstantMeta, cls).__new__(cls, name, bases, dct)

    def __setattr__(cls, key, value):
        raise TypeError('cannot set a value to Enum.')

    def __repr__(cls):
        return '<EnumConstant.%s>' % cls.__name__


class EnumConstant(object):
    __metaclass__ = EnumConstantMeta


class GOAL_TYPE(EnumConstant):
    IG_FOLLOW = 0
    IG_HASHTAG = 1
    IG_LIKE = 2
    IG_REGRAM = 3
    IG_SHARE = 4


class SOURCE_TYPE(EnumConstant):
    '''
    포인트 적립에 대한 카테고리
    0 ~ 99: 포인트 적립
    100 ~ : 포인트 사용
    '''
    MEMBER_JOIN = 1  # 회원 가입
    IG_HASHTAG = 11  # 인스타 해시태그 글쓰기에 대한 적립
    IG_LIKE = 12  # 인스타 좋아요에 대한 적립
    IG_REGRAM = 13  # 인스타 리그램에 대한 적립
    IG_SHARE = 14  # 인스타 공유에 대한 적립


GOAL_DESC = {
    GOAL_TYPE.IG_FOLLOW: '인스타그램 팔로우',
    GOAL_TYPE.IG_HASHTAG: '인스타그램 해시태그 글쓰기',
    GOAL_TYPE.IG_LIKE: '인스타그램 좋아요',
    GOAL_TYPE.IG_REGRAM: '인스타그램 리그램',
    GOAL_TYPE.IG_SHARE: '인스타그램 공유하기',
}


@main.context_processor
def inject_constants():
    return dict(
        GOAL_TYPE=GOAL_TYPE,
        GOAL_DESC=GOAL_DESC,
    )
