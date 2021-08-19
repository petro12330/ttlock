"""
WSGI config for ttlock_last project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

if config("DEBUG"):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttlock_last.settings')
else:
    import sys
    # путь к проекту, там где manage.py
    sys.path.insert(0, '/home/c/ci34005/django_lock/public_html/ttlock')
    # путь к фреймворку, там где settings.py
    sys.path.insert(0,
                    '/home/c/ci34005/django_lock/public_html/ttlock/ttlock_last')
    # путь к виртуальному окружению myenv
    # sys.path.insert(0, '/home/c/ci34005/django_lock/myenv/lib/python{0}/site-packages'.format(platform.python_version()[0:3]))
    sys.path.insert(0,
                    '/home/c/ci34005/django_lock/myenv/lib/python3.6/site-packages')
    os.environ["DJANGO_SETTINGS_MODULE"] = "ttlock_last.settings"

application = get_wsgi_application()
