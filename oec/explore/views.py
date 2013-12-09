import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec.db_attr.models import Country, Sitc, Hs
from oec import app, db, babel

mod = Blueprint('explore', __name__, url_prefix='/explore')

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<destination>/<product>/')
@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<destination>/<product>/<year>/')
def explore(app_name, classification, trade_flow, origin, destination, \
                product, year="2011"):
    g.page_type = mod.name
    # raise Exception(app_name, classification, trade_flow, origin, destination, product, year)
    return render_template("explore/index.html")
