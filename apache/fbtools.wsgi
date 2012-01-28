import os
import sys

path = '/srv/www'
if path not in sys.path:
    sys.path.insert(0, path)
fbtools_path = '/srv/www/fbtools'
if fbtools_path not in sys.path:
    sys.path.insert(0, fbtools_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fbtools.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

