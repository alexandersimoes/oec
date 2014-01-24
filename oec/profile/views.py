import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec import app, db, babel, view_cache, excluded_countries
from oec.utils import make_query
from oec.db_attr import models as attr_models
from oec.explore.models import Build, App
from sqlalchemy.sql.expression import func
from sqlalchemy import not_

mod = Blueprint('profile', __name__, url_prefix='/profile')

@mod.route('/country/')
def profile_country_redirect():
    Country = getattr(attr_models, "Country")
    c = Country.query.filter(Country.id_2char != None) \
                        .filter(not_(Country.id.in_(excluded_countries))) \
                        .order_by(func.random()).limit(1).first()
    
    return redirect(url_for(".profile_country", attr_id=c.id_3char))

@mod.route('/country/')
@mod.route('/country/<attr_id>/')
@view_cache.cached(timeout=None)
def profile_country(attr_id="usa"):
    g.page_type = mod.name
    
    attr = getattr(attr_models, "Country").query.filter_by(id_3char=attr_id).first()
    
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
                        year="2010")
    
    return render_template("profile/country.html", 
                                builds=builds,
                                attr=attr)

@mod.route('/<attr_type>/')
@mod.route('/<attr_type>/<attr_id>/')
@view_cache.cached(timeout=None)
def profile_product(attr_type, attr_id="usa"):
    g.page_type = mod.name
    
    if attr_type == "hs":
        attr = getattr(attr_models, attr_type.capitalize()).query.filter_by(hs=attr_id).first()
    else:
        attr = getattr(attr_models, attr_type.capitalize()).query.filter_by(sitc=attr_id).first()
    
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
                        year="2010")
    
    return render_template("profile/product.html", 
                                builds=builds,
                                attr=attr)
