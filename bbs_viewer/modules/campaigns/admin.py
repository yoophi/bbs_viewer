# -*- coding: utf8
from __future__ import unicode_literals

from flask import current_app
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from wtforms import SelectField

from instashare.constants import GOAL_TYPE
from instashare.database import db
from instashare.extensions import admin
from .models import Campaign, CampaignGoal


class CampaignGoalInlineModelForm(InlineFormAdmin):
    form_overrides = {
        'type': SelectField
    }
    form_args = {
        'type': {
            'choices':
                [
                    (GOAL_TYPE.IG_FOLLOW, '인스타그램 팔로우'),
                    (GOAL_TYPE.IG_HASHTAG, '인스타그램 해시태그 글쓰기'),
                    (GOAL_TYPE.IG_LIKE, '인스타그램 좋아요'),
                    (GOAL_TYPE.IG_REGRAM, '인스타그램 리그램'),
                    (GOAL_TYPE.IG_SHARE, '인스타그램 공유하기'),
                ],
            'coerce': int
        }

    }


class CampaignView(ModelView):
    column_auto_select_related = True
    inline_models = [
        CampaignGoalInlineModelForm(CampaignGoal),
    ]


admin.add_view(CampaignView(Campaign, db.session, name='캠페인', category='캠페인'))
