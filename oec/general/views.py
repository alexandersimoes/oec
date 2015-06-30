from operator import itemgetter
from datetime import datetime
from markdown import markdown
from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, jsonify, \
                    get_flashed_messages, Response
from flask.ext.babel import gettext

import oec
from oec.db_attr.models import Country, Country_name, Sitc, Sitc_name
from oec.db_attr.models import Hs92, Hs92_name, Hs96, Hs96_name
from oec.db_attr.models import Hs02, Hs02_name, Hs07, Hs07_name
from oec.explore.models import Build
from oec.general.search import Search

import time, urllib2, json
from dateutil import parser

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
    g.available_years = available_years

    # Save variable in session so we can determine if this is the user's
    # first time on the site
    # if 'first_time' in session:
    #     session['first_time'] = False
    # else:
    #     session['first_time'] = True
    #
    # if session['first_time'] and request.endpoint != "explore.embed" and request.endpoint != "general.home":
    #     flash("Welcome! We have recently redesigned the URL structure for the site to explicity include the language. The site should still function exactly the same as it had. <a href='https://github.com/alexandersimoes/oec/releases/tag/v2.2.0' target='_blank'>Read more about the implications of this update here</a>.", "first_time")

    lang = request.args.get('lang', None)
    if lang:
        g.locale = get_locale(lang)

    if request.endpoint != 'static':
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
    if lang != "en":
        session['new_lang'] = True
        flash_txt = '''We've noticed you've changed the language, if you see
        some translations that look odd and you think you could do better feel
        free to help us out by <a target="_blank" href="/about/translations/#{0}">
        adding your suggestions here</a>.'''.format(lang)
        flash(flash_txt, 'new_lang')
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home', lang=g.locale))

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
@mod.route('<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","zh"):lang>/')
def home(lang=None):
    if lang is None:
        return redirect(url_for('.home', lang=g.locale))
    g.page_type = "home"
    g.locale = get_locale(lang)

    '''get ramdom country'''
    c = Country.query.get(choice(random_countries))
    # exports tree map
    default_build = Build("tree_map", "hs92", "export", c, "all", "show")
    
    return render_template("home.html", default_build=default_build)

@mod.route('iframe_test/')
@mod.route('iframe_test/<lang>/')
def iframe_test(lang="en"):
    return render_template("iframe_test.html", lang=lang)

@mod.route('search/')
def search():
    query = request.args.get('q', '')
    results = {"items": Search(query).results()}
    return jsonify(results)

###############################
# API views
# ---------------------------
@mod.route('atlas/')
def atlas():
    g.page_type = "atlas"
    return render_template("atlas/index.html")

###############################
# About views
# ---------------------------
@mod.route('about/')
def about():
    return redirect(url_for('.about_team'))

@mod.route('about/team/')
def about_team():
    g.page_type = "about"
    g.sub_title = "team"
    return render_template("about/team.html")

@mod.route('about/data/')
def about_data_redirect():
    return redirect(url_for('.about_data_sources'))

@mod.route('about/data/sources/')
def about_data_sources():
    g.page_type = "about"
    g.sub_title = "data"
    return render_template("about/data_sources.html", data_type="sources")

@mod.route('about/data/download/')
def about_data_download():
    g.page_type = "about"
    g.sub_title = "data"
    return render_template("about/data_download.html", data_type="download")

@mod.route('about/data/<data_type>/')
def about_data(data_type):
    g.page_type = "about"
    g.sub_title = "data"
    lang = request.args.get('lang', g.locale)
    download = request.args.get('download', None)

    if data_type == "sitc":
        items = Sitc.query.filter(Sitc.sitc != None).order_by(Sitc.sitc).all()
        headers = ["SITC", "Name"]
        title = "SITC4 product names and codes"
        id_col = "sitc"
    elif data_type == "hs":
        items = Hs.query.filter(Hs.hs != None).order_by(Hs.hs).all()
        headers = ["HS", "Name"]
        title = "HS4 (harmonized system) product names and codes"
        id_col = "hs"
    elif data_type == "country":
        items = Country.query.filter(Country.id_3char != None).order_by(Country.id_3char).all()
        headers = ["Abbrv", "Name"]
        title = "Country names and abbreviations"
        id_col = "id_3char"

    if download:
        s = StringIO()
        writer = csv.writer(s)
        title = "{0}_classification_list".format(data_type)
        writer.writerow([unicode(h).encode("utf-8") for h in headers])
        for i in items:
            writer.writerow([getattr(i, id_col), unicode(i.get_name()).encode("utf-8")])
        content_disposition = "attachment;filename={0}.csv".format(title)
        return Response(s.getvalue(),
                            mimetype="text/csv;charset=UTF-8",
                            headers={"Content-Disposition": content_disposition})

    return render_template("about/data.html", items=items, headers=headers,
                            title=title, data_type=data_type, id_col=id_col)

@mod.route('about/permissions/')
def about_permissions():
    g.page_type = "about"
    g.sub_title = "permissions"
    return render_template("about/permissions.html")

@mod.route('about/faqs/')
def about_faqs():
    g.page_type = "about"
    g.sub_title = "faqs"
    return render_template("about/faqs.html")

@mod.route('about/translations/')
def about_translations():
    g.page_type = "about"
    g.sub_title = "translations"
    return render_template("about/translations.html")

@mod.route('about/updates/')
def about_updates():
    g.page_type = "about"
    g.sub_title = "updates"
    releases = json.load(urllib2.urlopen("https://api.github.com/repos/alexandersimoes/oec/releases"))
    updates = []
    for r in releases:
        u = {
            "title": r["name"],
            "body": markdown(r["body"]),
            "date": {
                "human": parser.parse(r["published_at"]).strftime("%A, %b %d %Y"),
                "meta": r["published_at"]
            },
            "url": r["html_url"]
        }
        updates.append(u)
    return render_template("about/updates.html", updates=updates)

###############################
# API views
# ---------------------------
@mod.route('about/api/')
def api():
    return redirect(url_for(".api_embed"))

@mod.route('about/api/embed/')
def api_embed():
    g.page_type = "about"
    g.sub_title = "api"
    return render_template("about/api_embed.html", data_type="embed")

@mod.route('about/api/data/')
def api_data():
    g.page_type = "about"
    g.sub_title = "api"
    return render_template("about/api_data.html", data_type="data")

###############################
# Legacy support views
# ---------------------------
@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def embed_legacy(app_name, trade_flow, origin, dest, product, year=2012):
    c = 'sitc' if int(year) < 1995 else 'hs'
    if product != "show" and product != "all":
        prod = Hs.query.filter_by(hs=product).first()
        c = 'hs'
        if not prod:
            c = 'sitc'
            prod = Sitc.query.filter_by(sitc=product).first()
        product = prod.id
    lang = request.args.get('lang', g.locale)
    redirect_url = url_for('explore.embed', lang=g.locale, app_name=app_name, \
                classification=c, trade_flow=trade_flow, origin_id=origin, \
                dest_id=dest, prod_id=product, year=year)
    return redirect(redirect_url+"?controls=false")

@mod.route('country/<country_id>/')
def profile_country_legacy(country_id):
    return redirect(url_for('profile.profile_country', attr_id=country_id))

@mod.route('hs4/<hs_id>/')
def profile_hs_legacy(hs_id):
    return redirect(url_for('profile.profile_product', attr_type="hs", \
                attr_id=hs_id))

@mod.route('sitc4/<sitc_id>/')
def profile_sitc_legacy(sitc_id):
    return redirect(url_for('profile.profile_product', attr_type="sitc", \
                attr_id=sitc_id))

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
