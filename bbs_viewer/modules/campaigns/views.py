# coding: utf8
from __future__ import unicode_literals

import random

from flask import render_template, request, flash, abort, url_for, redirect, \
    current_app, jsonify
from flask_login import login_required, current_user

from instashare.constants import GOAL_TYPE
from instashare.core import main
from instashare.database import db
from instashare.modules.campaigns.forms import CampaignForm, CampaignGoalForm
from instashare.modules.campaigns.schema import MediaSchema
from .models import Campaign, CampaignGoal


@main.route('/campaigns/create', methods=['GET', 'POST'])
@login_required
def campaign_create():
    form = CampaignForm(request.form)
    if request.method == 'POST' and form.validate():
        campaign = Campaign(user_id=current_user.id)
        form.populate_obj(campaign)
        db.session.add(campaign)
        try:
            db.session.commit()
            return 'SUCCESS'

        except Exception as e:
            flash(str(e))

    return render_template('campaigns/edit.html', form=form)


@main.route('/campaigns/<int:id>')
@login_required
def campaign_detail(id):
    campaign = Campaign.query.get(id)
    return render_template('campaigns/detail.html', campaign=campaign)


@main.route('/campaigns/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def campaign_edit(id):
    campaign = Campaign.query.get(id)
    if campaign.user_id != current_user.id:
        return abort(400)

    form = CampaignForm(request.form, campaign)

    if request.method == 'POST' and form.validate():
        form.populate_obj(campaign)
        db.session.add(campaign)

        try:
            db.session.commit()
            return redirect(url_for('main.campaign_detail', id=campaign.id))
        except Exception as e:
            flash(str(e))

    return render_template('campaigns/edit.html', campaign=campaign, form=form)


@main.route('/campaigns')
def campaigns():
    widths = [200, ]
    heights = [100, 200, 300, 400]

    rects = []
    for i in xrange(30):
        rects.append(
            {
                'width': random.choice(widths),
                'height': random.choice(heights)
            }
        )

    return render_template('campaigns/list.html', rects=rects)


@main.route('/my/campaigns')
@login_required
def my_campaigns():
    campaigns = Campaign.query.filter(
        Campaign.user_id == current_user.id
    )

    return render_template('campaigns/my_campaigns.html', campaigns=campaigns)


@main.route('/campaigns/<int:id>/goals/create', methods=['GET', 'POST'])
@login_required
def campaign_goal_create(id):
    campaign = Campaign.query.get(id)
    if campaign.user_id != current_user.id:
        return abort(400)

    form = CampaignGoalForm(request.form)
    if request.method == 'POST' and form.validate():
        goal = CampaignGoal(campaign_id=id)
        form.populate_obj(goal)

        db.session.add(goal)
        try:
            db.session.commit()
            return redirect(url_for('main.campaign_detail', id=id))
        except Exception as e:
            flash(str(e))

    return render_template('campaigns/edit_goal.html', campaign=campaign,
                           form=form)


@main.route('/campaigns/<int:id>/goals/<int:gid>/edit', methods=['GET', 'POST'])
@login_required
def campaign_goal_edit(id, gid):
    campaign = Campaign.query.get(id)
    if campaign.user_id != current_user.id:
        return abort(400)

    goal = CampaignGoal.query.filter(
        CampaignGoal.id == gid,
        CampaignGoal.campaign_id == id,
    ).first()

    if not goal:
        return abort(404)

    form = CampaignGoalForm(request.form, goal)
    if request.method == 'POST' and form.validate():
        form.populate_obj(goal)

        db.session.add(goal)
        try:
            db.session.commit()
            return redirect(url_for('main.campaign_detail', id=id))
        except Exception as e:
            flash(str(e))

    return render_template('campaigns/edit_goal.html', campaign=campaign,
                           form=form)


@main.route('/campaigns/<int:id>/goals/<int:gid>/delete', methods=['POST'])
@login_required
def campaign_goal_delete(id, gid):
    campaign = Campaign.query.get(id)
    if campaign.user_id != current_user.id:
        return abort(400)

    goal = CampaignGoal.query.filter(
        CampaignGoal.id == gid,
        CampaignGoal.campaign_id == id,
    ).first()

    if not goal:
        return abort(404)

    db.session.delete(goal)
    try:
        db.session.commit()
        flash('캠페인 목표를 삭제하였습니다.')
    except Exception as e:
        flash(str(e))

    return redirect(url_for('main.campaign_detail', id=id))


@main.route('/browse/instagram')
@login_required
def browse_instagram():
    api = current_app.social.instagram.get_api()
    recent_media, next_ = api.user_media_feed()
    print dir(recent_media[0].caption)

    schema = MediaSchema(many=True)

    return jsonify(schema.dump(recent_media).data)


@main.route('/campaigns/ongoing/likes')
@login_required
def campaigns_ongoing_likes():
    goals = CampaignGoal.query.filter(CampaignGoal.type == GOAL_TYPE.IG_LIKE)

    return render_template('campaigns/ongoing_likes.html', goals=goals)
