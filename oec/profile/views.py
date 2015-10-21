import time, urllib2, json
from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort
from flask.ext.babel import gettext
from sqlalchemy.sql.expression import func

from oec import app, db, babel, view_cache, random_countries, available_years, cache_timeout
from oec.utils import make_query, make_cache_key
from oec.db_attr import models as attr_models
from oec.general.views import get_locale
from sqlalchemy.sql.expression import func
from sqlalchemy import not_
from random import choice
from oec.profile.models import Country, Product

@app.route('/profile/country/')
def country_profile_redirect_nolang_noattr():
    return redirect(url_for('profile.profile_country_redirect', lang=g.locale))
@app.route('/profile/country/<attr_id>/')
def country_profile_redirect_nolang(attr_id=None):
    return redirect(url_for('profile.profile_country', lang=g.locale, attr_id=attr_id))

@app.route('/profile/<attr_type>/')
def prod_profile_redirect_nolang_noattr(attr_type=None, attr_id=None):
    return redirect(url_for('profile.profile_product_redirect', lang=g.locale, attr_type=attr_type))
@app.route('/profile/<attr_type>/<attr_id>/')
def prod_profile_redirect_nolang(attr_type=None, attr_id=None):
    return redirect(url_for('profile.profile_product', lang=g.locale, attr_type=attr_type, attr_id=attr_id))

mod = Blueprint('profile', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","vi","zh"):lang>/profile')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route('/country/')
def profile_country_redirect():
    '''fetch random country'''
    c = getattr(attr_models, "Country").query.get(choice(random_countries))
    return redirect(url_for(".profile_country", lang=g.locale, attr_id=c.id_3char))

@mod.route('/<any("sitc","hs92","hs96","hs02","hs07"):attr_type>/')
def profile_product_redirect(attr_type):
    '''fetch random product'''
    tbl = getattr(attr_models, attr_type.capitalize())
    p = tbl.query.filter(func.char_length(tbl.id)==6).order_by(func.random()).first_or_404()
    return redirect(url_for(".profile_product", lang=g.locale, attr_type=attr_type, attr_id=p.get_display_id()))

def sanitize(id_3char):
    msg = None
    if id_3char in ["nam", "lso", "bwa", "swz"]:
        c = getattr(attr_models, "Country").query.filter_by(id_3char=id_3char).first()
        redirect_id_3char = "zaf"
        msg = "{0} reports their trade under South Africa in the HS classification. ".format(c.get_name())
    elif id_3char in ["bel", "lux"]:
        c = getattr(attr_models, "Country").query.filter_by(id_3char=id_3char).first()
        redirect_id_3char = "blx"
        msg = "{0} reports their trade under Belgium-Luxembourg in the HS classification. ".format(c.get_name())

    if msg:
        redirect_url = url_for('.profile_country', attr_id=redirect_id_3char)
        flash(msg+"<script>redirect('"+redirect_url+"', 10)</script>")

@mod.route('/country/<attr_id>/')
@view_cache.cached(timeout=cache_timeout, key_prefix=make_cache_key)
def profile_country(attr_id="usa"):
    c = Country("hs92", attr_id)
    if not c.attr: abort(404)
    g.page_sub_type = "country"
    return render_template("profile/index.html", profile=c)

@mod.route('/<any("sitc","hs92","hs96","hs02","hs07"):attr_type>/<attr_id>/')
@view_cache.cached(timeout=cache_timeout, key_prefix=make_cache_key)
def profile_product(attr_type, attr_id="7108"):
    p = Product(attr_type, attr_id)
    if not p.attr: abort(404)
    g.page_sub_type = "product"
    return render_template("profile/index.html", profile=p)
