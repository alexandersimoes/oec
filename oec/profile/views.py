import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec import app, db, babel
from oec.utils import make_query
from oec.db_attr.models import Country, Sitc, Hs
from oec.explore.models import Build, App

mod = Blueprint('profile', __name__, url_prefix='/profile')

@mod.route('/country/')
@mod.route('/country/<origin_id>/')
def profile(origin_id="nausa"):
    g.page_type = mod.name
    
    entity = Country.query.filter_by(id=origin_id).first()
    
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
        b.set_options(origin=origin_id, 
                        dest=None, 
                        product=None, 
                        classification="hs", 
                        year="2010")
    
    return render_template("profile/index.html", 
                                builds=builds,
                                entity=entity)
