import os
from os import environ

# general flask library
from flask import Flask
# flask-sqlalchemy connector for database queries
from flask.ext.sqlalchemy import SQLAlchemy
# flask-babel for handling L18n and L10n
from flask.ext.babel import Babel
# for new filters, redis sessions
from utils import Momentjs, formatter, strip_html, jinja_split, \
                    RedisSessionInterface, format_currency, format_percent
from werkzeug.contrib.fixers import ProxyFix

''' Base directory of where the site is held '''
oec_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(oec_dir, 'html'))
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load default configuration from config.py
app.config.from_object('config')

# DB connection object
db = SQLAlchemy(app)

# Set session store as server side (Redis)
redis_sesh = RedisSessionInterface()
if redis_sesh.redis:
    app.session_interface = redis_sesh

# Global Latest Year Variables
__latest_year__ = {"sitc": 2012, "hs": 2011, "population": 2012}
available_years = {"sitc": range(1962, 2012), "hs": range(1995, 2012)}

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['momentjs'] = Momentjs
app.jinja_env.globals['format'] = formatter
app.jinja_env.filters['strip_html'] = strip_html
app.jinja_env.filters['split'] = jinja_split
app.jinja_env.filters['format_currency'] = format_currency
app.jinja_env.filters['format_percent'] = format_percent

# Load the modules for each different section of the site
''' data API view/models '''
from oec.db_attr.views import mod as db_attr_module
from oec.db_sitc.views import mod as db_sitc_module
from oec.db_hs.views import mod as db_hs_module
''' front facing views/models of site '''
from oec.general.views import mod as general_module
from oec.explore.views import mod as explore_module
from oec.profile.views import mod as profile_module
from oec.rankings.views import mod as rankings_module

''' Register these modules as blueprints '''
app.register_blueprint(db_attr_module)
app.register_blueprint(db_sitc_module)
app.register_blueprint(db_hs_module)

app.register_blueprint(general_module)
app.register_blueprint(explore_module)
app.register_blueprint(profile_module)
app.register_blueprint(rankings_module)
