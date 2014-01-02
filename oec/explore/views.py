import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec import app, db, babel
from oec.utils import make_query
from oec.db_attr.models import Country, Sitc, Hs
from oec.explore.models import Build, App

mod = Blueprint('explore', __name__, url_prefix='/explore')

@mod.route('/')
def explore_redirect():
    return redirect(url_for('.explore', app_name="tree_map", \
                classification="hs", trade_flow="export", origin="nausa", \
                dest="all", product="show", year="2010"))

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def explore(app_name, classification, trade_flow, origin, dest, \
                product, year="2011"):
    g.page_type = mod.name
    
    current_app = App.query.filter_by(type=app_name).first_or_404()
    build_filters = {"origin":origin,"dest":dest,"product":product}
    for bf_name, bf in build_filters.items():
        if bf != "show" and bf != "all":
            build_filters[bf_name] = "<" + bf_name + ">"
    
    # raise Exception(current_app, trade_flow, build_filters["origin"], build_filters["dest"], build_filters["product"])
    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow, 
                        origin=build_filters["origin"], dest=build_filters["dest"], 
                        product=build_filters["product"]).first_or_404()
    current_build.set_options(origin=origin, dest=dest, product=product, 
                                classification=classification, year=year)
    
    # raise Exception(current_build.top_stats(5)["entries"][0])
    
    '''Every possible build for accordion links'''
    all_builds = Build.query.all()
    for i, build in enumerate(all_builds):
        build.set_options(origin=origin, dest=dest, product=product, classification=classification, year=year)
    
    kwargs = {"trade_flow":trade_flow, "origin_id":origin, "dest_id":dest, "year":year}
    if classification == "sitc":
        kwargs["sitc_id"] = product
    else:
        kwargs["hs_id"] = product
        
    # raise Exception(make_query(current_build.get_tbl(), request.args, g.locale, **kwargs))
    # raise Exception(current_build.top_stats(20))
    
    return render_template("explore/index.html",
        current_build = current_build,
        all_builds = all_builds)

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/<year>/embed/')
def embed(app_name, classification, trade_flow, origin, dest, \
                product, year="2011"):

    current_app = App.query.filter_by(type=app_name).first_or_404()
    build_filters = {"origin":origin,"dest":dest,"product":product}
    for bf_name, bf in build_filters.items():
        if bf != "show" and bf != "all":
            build_filters[bf_name] = "<" + bf_name + ">"
    
    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow, 
                        origin=build_filters["origin"], dest=build_filters["dest"], 
                        product=build_filters["product"]).first_or_404()
    current_build.set_options(origin=origin, dest=dest, product=product, 
                                classification=classification, year=year)

    return render_template("explore/embed.html", current_build = current_build)