import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort
from flask.ext.babel import gettext
from sqlalchemy.sql.expression import func

from oec import app, db, babel, view_cache, random_countries, available_years
from oec.utils import make_query, make_cache_key
from oec.db_attr import models as attr_models
from oec.explore.models import Build, App
from sqlalchemy.sql.expression import func
from sqlalchemy import not_
from random import choice

mod = Blueprint('profile', __name__, url_prefix='/profile')

@mod.route('/country/')
def profile_country_redirect():
    Country = getattr(attr_models, "Country")
    '''fetch random country'''
    c = Country.query.get(choice(random_countries))

    return redirect(url_for(".profile_country", attr_id=c.id_3char))

@mod.route('/<attr_type>/')
def profile_product_redirect(attr_type):
    '''fetch random product'''
    if attr_type == "hs":
        p = getattr(attr_models, attr_type.capitalize()).query.order_by(func.random()).first_or_404()
    else:
        p = getattr(attr_models, attr_type.capitalize()).query.order_by(func.random()).first_or_404()

    return redirect(url_for(".profile_product", attr_type=attr_type, attr_id=p.get_display_id()))

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

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True

    sanitize(attr_id)
    
    attrs = getattr(attr_models, "Country_name").query.filter(func.char_length(getattr(attr_models, "Country_name").origin_id)==5).filter_by(lang=g.locale).order_by(getattr(attr_models, "Country_name").name).all()
    prev, attr, next = [None]*3
    for a in attrs:
        next = a
        if None not in [attr, next]:
            break
        if a.origin_id[2:] == attr_id:
            attr = a
        elif attr is None:
            prev = a
    
    if attr == next: next = None
    if prev: prev = prev.country
    if attr: attr = attr.country
    if next: next = next.country

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
        b.set_options(origin=attr,
                        dest=None,
                        product=None,
                        classification="hs",
                        year=available_years["country"][-1])

    return render_template("profile/country.html",
                                is_iOS=False,
                                builds=builds,
                                prev=prev,
                                attr=attr,
                                next=next)

@mod.route('/<attr_type>/')
@mod.route('/<attr_type>/<attr_id>/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def profile_product(attr_type, attr_id="usa"):
    g.page_type = mod.name
    g.page_sub_type = attr_type

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True
    
    tbl = getattr(attr_models, attr_type.capitalize())
    tbl_name = getattr(attr_models, attr_type.capitalize()+"_name")
    id_name = attr_type + "_id"

    attrs = tbl_name.query.filter(func.char_length(getattr(tbl_name, id_name))==6) \
                        .filter_by(lang=g.locale) \
                        .order_by(tbl_name.name).all()
    
    prev, attr, next = [None]*3
    for i, a in enumerate(attrs):
        next = a
        if None not in [attr, next]:
            break
        if getattr(a, id_name)[2:] == attr_id:
            attr = a
        elif attr is None:
            prev = a
    
    if attr == next: next = None
    if prev: prev = getattr(prev,attr_type)
    if attr: attr = getattr(attr,attr_type)
    if next: next = getattr(next,attr_type)

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
                        product=attr,
                        classification=attr_type,
                        year=available_years[attr_type][-1])

    return render_template("profile/product.html",
                                is_iOS=is_iOS,
                                builds=builds,
                                classification=attr_type,
                                prev=prev,
                                attr=attr,
                                next=next)
