from __future__ import print_function

from flask import current_app, render_template
from flask_login import login_required

from instashare.core import main


@main.route('/user/profile')
@login_required
def profile():
    return render_template(
        'user/profile.html',
        twitter_conn=current_app.social.twitter.get_connection(),
        instagram_conn=current_app.social.instagram.get_connection()
    )


@main.route('/twitter_login')
def twitter_login():
    return render_template('twitter_login.html')


@main.route('/dummy')
def dummy():
    print(current_app.social.instagram)
    api = current_app.social.instagram.get_api()
    print('api', api)
    recent_media, next_ = api.user_recent_media(user_id=86012, count=10)
    # print('res', res)
    # # return str(res)
    return render_template('dummy.html', recent_media=recent_media)
