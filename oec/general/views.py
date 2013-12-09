from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec.db_attr.models import Country

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
        g.locale = get_locale()

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    
    if lang:
        if lang in supported_langs:
            new_lang = lang
        else:
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
# General views 
# ---------------------------
@app.after_request
def after_request(response):
    return response
    
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
    g.page_type = "error404"
    return render_template('general/404.html', error = e), 404