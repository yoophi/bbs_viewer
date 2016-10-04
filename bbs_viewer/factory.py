import os
from os import path

from bbs_viewer.core import main
from bbs_viewer.database import mongo
from bbs_viewer.extensions import config, bootstrap, ma, admin
from bbs_viewer.middleware import MethodRewriteMiddleware
from bbs_viewer.modules.posts.admin import PostAdminView
from flask_api_app import FlaskApiApp
from flask_api_app.core.api import api


class BbViewApp(FlaskApiApp):
    pass


def create_app_min():
    app = BbViewApp(__name__)

    config.init_app(app)
    app.config.from_yaml(
        file_name='app.yaml',
        search_paths=['/etc/bbs_viewer', path.dirname(app.root_path)]
    )

    ma.init_app(app)
    mongo.init_app(app)

    return app


def create_app(config_name=None):
    if config_name:
        os.environ['FLASK_ENV'] = config_name

    app = create_app_min()
    app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

    app.init_extensions()

    from flask_debugtoolbar import DebugToolbarExtension
    debug_toolbar = DebugToolbarExtension()
    debug_toolbar.init_app(app)

    bootstrap.init_app(app)

    # views
    import bbs_viewer.modules.main.views

    # api
    import bbs_viewer.modules.posts.api

    # admin
    with app.app_context():
        admin.add_view(PostAdminView(mongo.db.scrapy_items, 'Post'))

    app.register_core_blueprint(api=api, main=main)

    return app
