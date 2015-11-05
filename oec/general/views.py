# -*- coding: utf-8 -*-
from operator import itemgetter
from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, jsonify, \
                    get_flashed_messages, Response
from flask.ext.babel import gettext

import oec
from oec.db_attr.models import Country, Country_name, Sitc, Sitc_name
from oec.db_attr.models import Hs92, Hs92_name, Hs96, Hs96_name
from oec.db_attr.models import Hs02, Hs02_name, Hs07, Hs07_name
from oec.visualize.models import Build, Short
from oec.general.search import Search
from oec.translations.lookup import get_translations

import time, urllib2, json

import csv
from cStringIO import StringIO
from random import choice

mod = Blueprint('general', __name__, url_prefix='/')

from oec import app, db, babel, random_countries, available_years

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():

    g.page_type = mod.name
    g.supported_langs = current_app.config.get('LANGUAGES')
    g.supported_langs = sorted(g.supported_langs.iteritems(), key=lambda x: x[1].lower())
    g.available_years = available_years
    g.cache_version = 11
    g.translations = json.dumps(get_translations())

    # Save variable in session so we can determine if this is the user's
    # first time on the site
    # if 'first_time' in session:
    #     session['first_time'] = False
    # else:
    #     session['first_time'] = True
    #
    # if session['first_time'] and request.endpoint != "explore.embed" and request.endpoint != "general.home":
    #     flash("Welcome! We have recently redesigned the URL structure for the site to explicity include the language. The site should still function exactly the same as it had. <a href='https://github.com/alexandersimoes/oec/releases/tag/v2.2.0' target='_blank'>Read more about the implications of this update here</a>.", "first_time")

    if request.endpoint != 'static':
        g.locale = get_locale()
        # raise Exception(g.locale)
        g.dir = "rtl" if g.locale in ("ar", "he") else "ltr"

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
    if lang != "en":
        session['new_lang'] = True
        flash_txt = '''We've noticed you've changed the language, if you see
        some translations that look odd and you think you could do better feel
        free to help us out by <a target="_blank" href="/about/translations/#{0}">
        adding your suggestions here</a>.'''.format(lang)
        flash(flash_txt, 'new_lang')
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('.home', lang=g.locale))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    g.page_type = "error"
    return render_template('general/error.html', error = e), 404

###############################
# General views
# ---------------------------
@mod.route('/')
@mod.route('<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","vi","zh"):lang>/')
def home(lang=None):
    if not lang:
        return redirect(url_for('.home', lang='en'))
    g.page_type = "home"
    g.locale = get_locale(lang)
    return render_template("home.html")

@mod.route('iframe_test/')
@mod.route('iframe_test/<lang>/')
def iframe_test(lang="en"):
    return render_template("iframe_test.html", lang=lang)

@mod.route('search/')
def search():
    search_args = {}
    search_args["text"] = request.args.get('q', '')
    search_args["mode"] = request.args.get('mode', None)
    search_args["data_filter"] = request.args.get('filter', None)
    search_args = {k:v for k, v in search_args.items() if v}
    search_results = Search(**search_args).results()
    return jsonify(search_results)

@mod.route('api/')
def api():
    g.page_type = "api"
    return render_template("general/api.html")

@mod.route("publications/")
def publications():
    g.page_type = "publications"
    return render_template("general/publications.html")

@mod.route('explore/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('explore/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def explore_legacy_redir(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year=None):
    redirect_url = url_for('visualize.visualize', lang=g.locale, app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                    year=year)
    return redirect(redirect_url)

@mod.route('explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def embed_legacy_redir(app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year=available_years['hs92'][-1]):
    return redirect(url_for('visualize.embed', lang=g.locale, app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year))

@mod.route('<lang>/explore/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('<lang>/explore/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def explore_lang_legacy_redir(lang, app_name, classification, trade_flow, origin_id, dest_id, prod_id, year=None):
    redirect_url = url_for('visualize.visualize', lang=lang, app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                    year=year)
    return redirect(redirect_url)

@mod.route('<lang>/explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('<lang>/explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def embed_lang_legacy_redir(lang, app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year=available_years['hs92'][-1]):
    return redirect(url_for('visualize.embed', lang=lang, app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year))

@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def embed_legacy(app_name, trade_flow, origin, dest, product, year=2012):
    c = 'sitc' if int(year) < 1995 else 'hs92'
    if product != "show" and product != "all":
        prod = Hs92.query.filter_by(hs92=product).first()
        c = 'hs92'
        if not prod:
            c = 'sitc'
            prod = Sitc.query.filter_by(sitc=product).first()
        product = prod.get_display_id()
    lang = request.args.get('lang', g.locale)
    redirect_url = url_for('visualize.embed', lang=g.locale, app_name=app_name, \
                classification=c, trade_flow=trade_flow, origin_id=origin, \
                dest_id=dest, prod_id=product, year=[year])
    return redirect(redirect_url+"?controls=false")

@mod.route('country/<country_id>/')
def profile_country_legacy(country_id):
    return redirect(url_for('profile.profile_country', lang=g.locale, attr_id=country_id))

@mod.route('hs4/<hs_id>/')
def profile_hs_legacy(hs_id):
    return redirect(url_for('profile.profile_product', lang=g.locale, attr_type="hs92", attr_id=hs_id))

@mod.route('sitc4/<sitc_id>/')
def profile_sitc_legacy(sitc_id):
    return redirect(url_for('profile.profile_product', lang=g.locale, attr_type="sitc", attr_id=sitc_id))

###############################
# Handle shortened URLs
# ---------------------------
@mod.route('close/')
def close():
  return render_template("general/close.html")

###############################
# Handle shortened URLs
# ---------------------------
@mod.route('<slug>/')
def redirect_short_url(slug):
    short = Short.query.filter_by(slug = slug).first_or_404()
    short.clicks += 1
    short.last_accessed = datetime.utcnow()
    db.session.add(short)
    db.session.commit()

    return redirect(short.long_url)

###############################
# Legacy static views (redirects)
# ---------------------------
@mod.route('atlas/')
def legacy_atlas():
    return redirect(url_for(".publications"))

@mod.route('about/api/')
@mod.route('about/api/<path:legacy_path>')
def legacy_about_api(legacy_path=None):
    return redirect(url_for(".api"))

@mod.route('about/data/')
@mod.route('about/data/<path:legacy_path>')
def legacy_about_data(legacy_path=None):
    return redirect(url_for('resources.data', lang=g.locale))

@mod.route('about/permissions/')
def legacy_about_permissions():
    return redirect(url_for('resources.permissions', lang=g.locale))

@mod.route('about/faqs/')
def legacy_about_faqs():
    return redirect(url_for('resources.faqs', lang=g.locale))

@mod.route('about/')
@mod.route('about/<path:legacy_path>')
def legacy_about(legacy_path=None):
    return redirect(url_for('resources.about', lang=g.locale))
