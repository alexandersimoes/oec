import os
from os import environ

# general flask library
from flask import Flask
# flask-sqlalchemy connector for database queries
from flask.ext.sqlalchemy import SQLAlchemy
# flask-babel for handling L18n and L10n
from flask.ext.babel import Babel
# for new filters
from utils import Momentjs, formatter, strip_html, jinja_split, format_currency, \
                    format_percent, langify
from werkzeug.contrib.fixers import ProxyFix
# for caching views
from flask.ext.cache import Cache
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

# set up cache for views
view_cache = Cache(app)

# Global Latest Year Variables
available_years = {"sitc": range(1962, 2014), "hs92": range(1995, 2014), \
                    "hs96": range(1998, 2014), "hs02": range(2003, 2014), \
                    "hs07": range(2008, 2013), "country": range(1962, 2014)}

# Global for excluded countries
excluded_countries = ["ocglp", "xxwld", "asymd", "eumco", "saguf", "euksv", \
    "nabes", "nacuw", "navir", "eusjm", "namaf", "naant", "afreu", "afssd", \
    "afmyt", "eufro", "eubel", "eulux", "afswz", "afbwa", "aflso", "afnam", \
    "napri", "namtq", "euimn", "eulie", "euddr", "eufdr"]
random_countries = ["afago","afdza","afegy","afmar","afnga","afzaf","asare", \
    "asaze","asbgd","aschn","ashkg","asidn","asind","asirn","asirq","asisr", \
    "asjpn","askaz","askor","askwt","asmys","asomn","aspak","asphl","asqat", \
    "asrus","assau","assgp","astha","astur","astwn","asvnm","euaut", \
    "eubgr","eublr","eublx","euche","eucze","eudeu","eudnk","euesp","eufin", \
    "eufra","eugbr","eugrc","euhun","euirl","euita","eultu","eunld","eunor", \
    "eupol","euprt","eurou","eusvk","eusvn","euswe","euukr","nacan","nacri", \
    "namex","nausa","ocaus","ocnzl","saarg","sabra","sachl","sacol","saecu", \
    "saper","saven"]

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['momentjs'] = Momentjs
app.jinja_env.globals['format'] = formatter
app.jinja_env.filters['strip_html'] = strip_html
app.jinja_env.filters['split'] = jinja_split
app.jinja_env.filters['format_currency'] = format_currency
app.jinja_env.filters['format_percent'] = format_percent
app.jinja_env.filters['langify'] = langify

# Load the modules for each different section of the site
''' data API view/models '''
from oec.db_attr.views import mod as db_attr_module
# from oec.db_sitc.views import mod as db_sitc_module
# from oec.db_hs.views import mod as db_hs_module
from oec.db_data.views import mod as db_data_module
''' front facing views/models of site '''
from oec.general.views import mod as general_module
from oec.explore.views import mod as explore_module
from oec.profile.views import mod as profile_module
from oec.rankings.views import mod as rankings_module

''' Register these modules as blueprints '''
app.register_blueprint(db_attr_module)
# app.register_blueprint(db_sitc_module)
# app.register_blueprint(db_hs_module)
app.register_blueprint(db_data_module)

app.register_blueprint(general_module)
app.register_blueprint(explore_module)
app.register_blueprint(profile_module)
app.register_blueprint(rankings_module)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
