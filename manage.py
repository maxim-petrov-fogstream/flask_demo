#!/usr/bin/env python
import os
import subprocess
import sys

import sentry_sdk
from flask_script import Manager
from setproctitle import setproctitle

from expedition_merman_wrapper import create_app
from expedition_merman_wrapper.events.firebird_events_listener import (
    FirebirdEventsListener
)

APP_NAME = 'expedition_merman_wrapper'

app = create_app(APP_NAME)
manager = Manager(app)
setproctitle(APP_NAME)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port')
def runserver(host='0.0.0.0', port=None):
    """Запуск легковесного web-сервера для раработки на локальной машине."""
    default_port = app.config['PORT']
    if host == 'localhost':
        host = '127.0.0.1'
    port = port if port else default_port
    app.run(debug=True, host=host, port=int(port))


@manager.command
def run_celery():
    ret = subprocess.call(
        [
            'celery', 'worker',
            '-A', f'{APP_NAME}.celery_worker.celery',
            '--loglevel=info', '--concurrency=1'
        ]
    )
    sys.exit(ret)


@manager.command
def run_firebird_events_listener():
    sentry_dsn = os.getenv('SENTRY_DSN', None)
    if sentry_dsn:
        sentry_sdk.init(sentry_dsn)

    listener = FirebirdEventsListener()
    listener.update_db_schema()
    listener.run()


@manager.command
def uwsgi():
    """Запуск uwsgi."""
    os.execvp('uwsgi', ('--ini', 'uwsgi/uwsgi.ini',))


if __name__ == '__main__':
    manager.run()
