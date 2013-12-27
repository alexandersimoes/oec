import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.babel import gettext

from oec import app, db, babel
from oec.db_attr.models import Yo
from oec.db_hs.models import Yp as Yp_hs
from oec.db_sitc.models import Yp as Yp_sitc

mod = Blueprint('rankings', __name__, url_prefix='/rankings')

@mod.route('/')
def rankings_redirect():
    return redirect(url_for('.rankings', category="country"))

@mod.route('/<category>/')
@mod.route('/<category>/<int:year>/')
def rankings(category, year=2010):
    g.page_type = mod.name
    clamped_year = max(1962, min(year, 2011))
    if clamped_year != year:
        return redirect(url_for('.profile', category="country", year=clamped_year))
    
    cols = ["Rank", "Abbrv", "Country", "ECI Value"]
    tbl = Yo
    val_col = "eci"
    if category == "sitc":
        cols = ["Rank", "SITC", "Product", "PCI Value"]
        tbl = Yp_sitc
        val_col = "pci"
    elif category == "hs":
        cols = ["Rank", "HS", "Product", "PCI Value"]
        tbl = Yp_hs
        val_col = "pci"
    
    rankings = tbl.query.filter_by(year=clamped_year) \
                        .filter(getattr(tbl, val_col) != None) \
                        .order_by(getattr(tbl, "{0}_rank".format(val_col))) \
                        .all()
    
    return render_template("rankings/index.html",
                                category=category,
                                year=clamped_year,
                                cols=cols,
                                rankings=rankings)
