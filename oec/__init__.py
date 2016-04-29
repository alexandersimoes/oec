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
                    format_percent, langify, num_format, YearConverter
from werkzeug.contrib.fixers import ProxyFix
# for caching views
from flask.ext.cache import Cache
from werkzeug.contrib.fixers import ProxyFix

from config import DEBUG

from opbeat.contrib.flask import Opbeat

''' Base directory of where the site is held '''
oec_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(oec_dir, 'html'))
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load default configuration from config.py
app.config.from_object('config')

cache_timeout = 604800
if DEBUG:
    from flask.ext.scss import Scss
    Scss(app)
    # override cache timeout
    cache_timeout = 0

from flask.ext.assets import Environment, Bundle
assets = Environment(app)
assets.load_path.append(os.path.join(oec_dir, "assets/js/"))
js = Bundle("warning.js", "visualization.js", "configs/*.js", "helpers/*.js", output="js/visualization.js")
assets.register("js", js)

# DB connection object
db = SQLAlchemy(app)

# set up cache for views
view_cache = Cache(app)

# Global Latest Year Variables
available_years = {"sitc": range(1962, 2015), "hs92": range(1995, 2015), \
                    "hs96": range(1998, 2015), "hs02": range(2003, 2015), \
                    "hs07": range(2008, 2015), "country": range(1962, 2015)}

# Global for excluded countries
excluded_countries = ["ocglp", "xxwld", "asymd", "eumco", "saguf", "euksv", \
    "nabes", "nacuw", "navir", "eusjm", "namaf", "naant", "afreu", "afssd", \
    "afmyt", "eufro", "eubel", "eulux", "afswz", "afbwa", "aflso", "afnam", \
    "napri", "namtq", "euimn", "eulie", "euddr", "eufdr", "nablm", "eusun", \
    "euscg", "euyug"]
random_countries = ["afago","afdza","afegy","afmar","afnga","afzaf","asare", \
    "asaze","asbgd","aschn","ashkg","asidn","asind","asirn","asirq","asisr", \
    "asjpn","askaz","askor","askwt","asmys","asomn","aspak","asphl","asqat", \
    "eurus","assau","assgp","astha","astur","astwn","asvnm","euaut", \
    "eubgr","eublr","eublx","euche","eucze","eudeu","eudnk","euesp","eufin", \
    "eufra","eugbr","eugrc","euhun","euirl","euita","eultu","eunld","eunor", \
    "eupol","euprt","eurou","eusvk","eusvn","euswe","euukr","nacan","nacri", \
    "namex","nausa","ocaus","ocnzl","saarg","sabra","sachl","sacol","saecu", \
    "saper","saven"]
earliest_data = {"afago":1985,"afbdi":1980,"afben":1980,"afbfa":1980,"afbwa":1980,"afcaf":1980,"afciv":1980,"afcmr":1980,"afcod":1980,"afcog":1980,"afcom":1980,"afcpv":1980,"afdji":1990,"afdza":1980,"afegy":1980,"aferi":1992,"afeth":1981,"afgab":1980,"afgha":1980,"afgin":1986,"afgmb":1980,"afgnb":1980,"afgnq":1980,"afken":1980,"aflbr":1980,"aflby":1995,"aflso":1980,"afmar":1980,"afmdg":1980,"afmli":1980,"afmoz":1980,"afmrt":1980,"afmus":1980,"afmwi":1980,"afnam":1980,"afner":1980,"afnga":1980,"afrwa":1980,"afsdn":1980,"afsen":1980,"afsle":1980,"afssd":2008,"afstp":2000,"afswz":1980,"afsyc":1980,"aftcd":1980,"aftgo":1980,"aftun":1980,"aftza":1988,"afuga":1982,"afzaf":1980,"afzmb":1980,"afzwe":1980,"asafg":2001,"asare":1980,"asarm":1990,"asaze":1990,"asbgd":1980,"asbhr":1980,"asbrn":1980,"asbtn":1980,"aschn":1980,"ascyp":1980,"asgeo":1980,"ashkg":1980,"asidn":1980,"asind":1980,"asirn":1980,"asirq":2000,"asisr":1980,"asjor":1980,"asjpn":1980,"askaz":1990,"askgz":1986,"askhm":1993,"askor":1980,"askwt":1992,"aslao":1984,"aslbn":1988,"aslka":1980,"asmac":1982,"asmdv":1995,"asmng":1981,"asmys":1980,"asnpl":1980,"asomn":1980,"aspak":1980,"asphl":1980,"aspse":1994,"asqat":1995,"assau":1980,"assgp":1980,"assyr":1980,"astha":1980,"astjk":1985,"astkm":1987,"astls":1999,"astur":1980,"asuzb":1987,"asvnm":1984,"asyem":1990,"eualb":1980,"euand":1980,"euaut":1980,"eubel":1980,"eubgr":1980,"eubih":1994,"eublr":1990,"euche":1980,"eucze":1990,"eudeu":1991,"eudnk":1980,"euesp":1980,"euest":1993,"eufin":1980,"eufra":1980,"eufro":1998,"eugbr":1980,"eugrc":1980,"euhrv":1995,"euhun":1980,"euimn":1984,"euirl":1980,"euisl":1980,"euita":1980,"euksv":2000,"eulie":1980,"eultu":1993,"eulux":1980,"eulva":1993,"eumco":1980,"eumda":1980,"eumkd":1990,"eumlt":1980,"eumne":1997,"eunld":1980,"eunor":1980,"eupol":1990,"euprt":1980,"eurou":1980,"eurus":1989,"eusmr":2000,"eusrb":1989,"eusvk":1994,"eusvn":1994,"euswe":1980,"euukr":1987,"naabw":1994,"naatg":1980,"nabhs":1980,"nablz":1980,"nabmu":1980,"nabrb":1980,"nacan":1980,"nacri":1980,"nacub":1980,"nacym":1996,"nadma":1980,"nadom":1980,"nagrd":1980,"nagrl":1980,"nagtm":1980,"nahnd":1980,"nahti":1995,"najam":1995,"nakna":1980,"nalca":1980,"namex":1980,"nanic":1980,"napan":1980,"napri":1980,"naslv":1980,"natto":1980,"nausa":1980,"navct":1980,"ocaus":1980,"ocfji":1980,"ocfsm":1986,"ockir":1980,"ocmhl":1981,"ocncl":1995,"ocnzl":1980,"ocplw":1991,"ocpng":1980,"ocpyf":1995,"ocslb":1990,"octon":1981,"octuv":1990,"ocvut":1980,"ocwsm":1982,"saarg":1980,"sabol":1980,"sabra":1980,"sachl":1980,"sacol":1980,"saecu":1980,"saguy":1980,"saper":1980,"sapry":1980,"sasur":1980,"saury":1980,"saven":1980,"xxwld":1980}

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
app.jinja_env.filters['num_format'] = num_format

# add custom url arg converter
app.url_map.converters['year'] = YearConverter

# Load the modules for each different section of the site
for view in ["db_attr", "db_data", "general", "profile", "rankings", "resources", "visualize"]:
    mod = __import__("oec.{}.views".format(view), fromlist=["mod"])
    mod = getattr(mod, "mod")
    app.register_blueprint(mod)

app.wsgi_app = ProxyFix(app.wsgi_app)

# opbeat initialization
opbeat = Opbeat(app)

if __name__ == '__main__':
    app.run()
