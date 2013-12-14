from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec.db_attr.models import Country, Sitc, Hs

import time, urllib2, json

mod = Blueprint('general', __name__, url_prefix='/')

from oec import app, db, babel

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    g.color = "#af1f24"
    g.page_type = mod.name
    g.supported_langs = current_app.config.get('LANGUAGES')
    
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
    
    # Set the locale to either 'pt' or 'en' on the global object
    if request.endpoint != 'static':
        # g.locale = "hi"
        # raise Exception(g.locale)
        g.locale = get_locale()

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    
    if lang:
        if lang in supported_langs:
            new_lang = lang
        session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif 'locale' in session:
            new_lang = session['locale']
        else:
            session['locale'] = new_lang
    
    return new_lang

###############################
# Set language views 
# ---------------------------
@mod.route('set_lang/<lang>/')
def set_lang(lang):
    g.locale = get_locale(lang)
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    return "404"
    # g.page_type = "error404"
    # return render_template('general/404.html', error = e), 404

###############################
# General views 
# ---------------------------
@mod.route('/')
def home():
    g.page_type = "home"
    ip = request.remote_addr
    
    # fetch the url
    url = "http://api.hostip.info/get_json.php?ip="+ip
    json_response = json.loads(urllib2.urlopen(url).read())
    country_code = json_response["country_code"]
    
    c = Country.query.filter_by(id_2char=country_code).first()
    if c is None:
        c = Country.query.filter_by(id="nausa").first()
    
    return render_template("home.html", default_country=c)

###############################
# API views 
# ---------------------------
@mod.route('book/')
def book():
    g.page_type = "book"
    return render_template("book/index.html")

###############################
# About views 
# ---------------------------
@mod.route('about/')
def about():
    g.page_type = "about"
    return render_template("about/index.html")

@mod.route('about/data/')
def about_data_redirect():
    return redirect(url_for('.about_data', data_type="sitc"))

@mod.route('about/data/<data_type>/')
def about_data(data_type):
    lang = request.args.get('lang', g.locale)
    
    if data_type == "sitc":
        items = Sitc.query.all()
        headers = ["Name", "SITC4 Code"]
        title = "SITC4 product names and codes"
    elif data_type == "hs":
        items = Hs.query.all()
        headers = ["Name", "HS4 Code"]
        title = "HS4 (harmonized system) product names and codes"
    elif data_type == "country":
        items = Country.query.all()
        headers = ["Name", "Alpha 3 Abbreviation"]
        title = "Country names and abbreviations"
    
    return render_template("about/data.html", items=items, headers=headers, title=title)

@mod.route('about/team/')
def about_team():
    return render_template("about/team.html")

@mod.route('about/permissions/')
def about_permissions():
    return render_template("about/permissions.html")

###############################
# API views 
# ---------------------------
@mod.route('api/')
def api():
    return redirect(url_for(".api_embed"))

@mod.route('api/embed/')
def api_embed():
    g.page_type = "api"
    return render_template("api/embed.html")

@mod.route('api/data/')
def api_data():
    g.page_type = "api"
    return render_template("api/data.html")