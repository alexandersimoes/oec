import os, sys
 
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
 
sys.path.append('/usr/local/lib/python2.6/dist-packages/django/')
sys.path.append('/home/macro/public_html/atlas_economic_complexity/django_files')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'atlas.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
