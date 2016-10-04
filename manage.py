# coding: utf-8

from __future__ import unicode_literals, print_function

from flask_migrate import MigrateCommand, Migrate
from flask_script import Server, Manager
from flask_script.commands import Shell, ShowUrls

from bbs_viewer.database import db
from bbs_viewer.factory import create_app

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


# Turn on debugger by default and reloader
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True,
                                        host='0.0.0.0'))

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('show_urls', ShowUrls)

# extra commands
# from instashare.core.accounts.commands import *
# from instashare.modules.media.commands import *

if __name__ == "__main__":
    manager.run()
