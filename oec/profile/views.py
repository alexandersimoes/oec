import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort
from flask.ext.babel import gettext
from sqlalchemy.sql.expression import func

from oec import app, db, babel, view_cache, random_countries, available_years
from oec.utils import make_query, make_cache_key
from oec.db_attr import models as attr_models
from oec.explore.models import Build, App
from oec.general.views import get_locale
from sqlalchemy.sql.expression import func
from sqlalchemy import not_
from random import choice

@app.route('/profile/country/')
@app.route('/profile/country/<attr_id>/')
def country_profile_redirect_nolang(attr_id=None):
    return redirect(url_for('profile.profile_country', lang=g.locale, attr_id=attr_id))

@app.route('/profile/<attr_type>/')
@app.route('/profile/<attr_type>/<attr_id>/')
def prod_profile_redirect_nolang(attr_id=None):
    return redirect(url_for('profile.profile_product', lang=g.locale, attr_type=attr_type, attr_id=attr_id))

mod = Blueprint('profile', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","zh"):lang>/profile')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.route('/country/')
def profile_country_redirect():
    Country = getattr(attr_models, "Country")
    '''fetch random country'''
    c = Country.query.get(choice(random_countries))

    return redirect(url_for(".profile_country", lang=g.locale, attr_id=c.id_3char))

@mod.route('/<attr_type>/')
def profile_product_redirect(attr_type):
    '''fetch random product'''
    if attr_type == "hs":
        p = getattr(attr_models, attr_type.capitalize()).query.order_by(func.random()).first_or_404()
    else:
        p = getattr(attr_models, attr_type.capitalize()).query.order_by(func.random()).first_or_404()

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

@mod.route('/country/')
@mod.route('/country/<attr_id>/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def profile_country(attr_id="usa"):
    g.page_type = mod.name
    g.page_sub_type = "country"
    c_tbl = getattr(attr_models, "Country")
    cname_tbl = getattr(attr_models, "Country_name")

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True

    sanitize(attr_id)
    
    this_country = c_tbl.query.filter_by(id_3char=attr_id).first_or_404()
    attrs=db.session.query(c_tbl, cname_tbl.name) \
            .filter(c_tbl.id_3char!=None) \
            .filter(cname_tbl.origin_id==getattr(attr_models, "Country").id) \
            .filter(cname_tbl.lang==g.locale) \
            .order_by(cname_tbl.name).all()
    attrs = [a[0] for a in attrs]
    this_country_index = attrs.index(this_country)
    prev_country = attrs[this_country_index-1] if this_country_index>0 else None
    next_country = attrs[this_country_index+1] if this_country_index<(len(attrs)-1) else None

    tree_map = App.query.filter_by(type="tree_map").first()

    exports = Build.query.filter_by(app=tree_map,
                                            trade_flow="export",
                                            origin="<origin>",
                                            dest="all",
                                            product="show").first()

    imports = Build.query.filter_by(app=tree_map,
                                            trade_flow="import",
                                            origin="<origin>",
                                            dest="all",
                                            product="show").first()

    destinations = Build.query.filter_by(app=tree_map,
                                            trade_flow="export",
                                            origin="<origin>",
                                            dest="show",
                                            product="all").first()

    origins = Build.query.filter_by(app=tree_map,
                                            trade_flow="import",
                                            origin="<origin>",
                                            dest="show",
                                            product="all").first()

    builds = [exports, imports, destinations, origins]
    for b in builds:
        b.set_options(origin=this_country,
                        dest=None,
                        product=None,
                        classification="hs",
                        year=available_years["country"][-1])

    return render_template("profile/country.html",
                                is_iOS=False,
                                builds=builds,
                                prev=prev_country,
                                attr=this_country,
                                next=next_country)

@mod.route('/<attr_type>/')
@mod.route('/<attr_type>/<attr_id>/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def profile_product(attr_type, attr_id="7108"):
    g.page_type = mod.name
    g.page_sub_type = attr_type
    p_tbl = getattr(attr_models, attr_type.capitalize())
    pname_tbl = getattr(attr_models, attr_type.capitalize()+"_name")
    pid_name = attr_type + "_id"

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True
    
    this_prod = p_tbl.query.filter(getattr(p_tbl, attr_type)==attr_id).first_or_404()
    attrs=db.session.query(p_tbl, pname_tbl.name) \
            .filter(func.char_length(p_tbl.id)==6) \
            .filter(getattr(pname_tbl, pid_name)==p_tbl.id) \
            .filter(pname_tbl.lang==g.locale) \
            .order_by(pname_tbl.name).all()
    attrs = [a[0] for a in attrs]
    this_prod_index = attrs.index(this_prod)
    prev_prod = attrs[this_prod_index-1] if this_prod_index>0 else None
    next_prod = attrs[this_prod_index+1] if this_prod_index<(len(attrs)-1) else None

    tree_map = App.query.filter_by(type="tree_map").first()

    exports = Build.query.filter_by(app=tree_map,
                                            trade_flow="export",
                                            origin="show",
                                            dest="all",
                                            product="<product>").first()

    imports = Build.query.filter_by(app=tree_map,
                                            trade_flow="import",
                                            origin="show",
                                            dest="all",
                                            product="<product>").first()

    builds = [exports, imports]
    for b in builds:
        b.set_options(origin=None,
                        dest=None,
                        product=this_prod,
                        classification=attr_type,
                        year=available_years[attr_type][-1])

    return render_template("profile/product.html",
                                is_iOS=is_iOS,
                                builds=builds,
                                classification=attr_type,
                                prev=prev_prod,
                                attr=this_prod,
                                next=next_prod)
