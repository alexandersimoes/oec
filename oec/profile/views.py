import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

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
@view_cache.cached(timeout=2592000, key_prefix=make_cache_key)
def profile_country(attr_id="usa"):
    g.page_type = mod.name

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True

    sanitize(attr_id)

    attr = getattr(attr_models, "Country").query.filter_by(id_3char=attr_id).first_or_404()

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
                                attr=attr)

@mod.route('/<attr_type>/')
@mod.route('/<attr_type>/<attr_id>/')
@view_cache.cached(timeout=None, key_prefix=make_cache_key)
def profile_product(attr_type, attr_id="usa"):
    g.page_type = mod.name

    is_iOS = False
    if any(x in request.headers.get('User-Agent') for x in ["iPad","iPhone","iPod"]):
        is_iOS = True

    if attr_type == "hs":
        attr = getattr(attr_models, attr_type.capitalize()).query.filter_by(hs=attr_id).first_or_404()
    else:
        attr = getattr(attr_models, attr_type.capitalize()).query.filter_by(sitc=attr_id).first_or_404()

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
                                attr=attr)
