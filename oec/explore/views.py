import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec.db_attr.models import Country, Sitc, Hs
from oec.explore.models import Build, App
from oec import app, db, babel

mod = Blueprint('explore', __name__, url_prefix='/explore')

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
    
    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow, 
                        origin=build_filters["origin"], dest=build_filters["dest"], 
                        product=build_filters["product"]).first_or_404()
    current_build.set_options(origin=origin, dest=dest, product=product, 
                                classification=classification)
    
    '''Every possible build for accordion links'''
    all_builds = Build.query.all()
    for build in all_builds:
        build.set_options(origin=origin, dest=dest, product=product, classification=classification)

    return render_template("explore/index.html",
        current_build=current_build)
