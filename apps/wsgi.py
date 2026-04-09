import sys, os

# Chemin vers le dossier contenant manage.py
sys.path.insert(0, '/home/c2320352c/public_html/ap')

# Nom exact du projet Django (dossier contenant settings.py)
os.environ['DJANGO_SETTINGS_MODULE'] = 'apps.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
