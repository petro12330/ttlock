import os
import sys
import platform
#путь к проекту, там где manage.py
sys.path.insert(0, '/home/c/ci34005/django_lock/public_html/ttlock')
#путь к фреймворку, там где settings.py
sys.path.insert(0, '/home/c/ci34005/django_lock/public_html/ttlock/ttlock_last')
#путь к виртуальному окружению myenv
#sys.path.insert(0, '/home/c/ci34005/django_lock/myenv/lib/python{0}/site-packages'.format(platform.python_version()[0:3]))
sys.path.insert(0, '/home/c/ci34005/django_lock/myenv/lib/python3.6/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "ttlock_last.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()