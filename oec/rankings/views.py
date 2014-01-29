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
def rankings(category=None,year=None):
    
    g.page_type = mod.name
    
    if category == None:
        category = "country"
    
    if category == "sitc":
        years = range(1962, 2011)
        cols = ["Rank", "SITC", "Product", "PCI Value"]
        tbl = Yp_sitc
        val_col = "pci"
    elif category == "hs":
        years = range(1995, 2012)
        cols = ["Rank", "HS", "Product", "PCI Value"]
        tbl = Yp_hs
        val_col = "pci"
    elif category == "country":
        years = range(1962, 2011)
        cols = ["Rank", "Abbrv", "Country", "ECI Value"]
        tbl = Yo
        val_col = "eci"
        
    if year == None:
        year = years[-1]
    elif year > years[-1]:
        return redirect(url_for('.rankings', category=category, year=years[0]))
    elif year < years[0]:
        return redirect(url_for('.rankings', category=category, year=years[-1]))
    
    rankings = tbl.query.filter_by(year=year) \
                        .filter(getattr(tbl, val_col) != None) \
                        .order_by(getattr(tbl, "{0}_rank".format(val_col))) \
                        .all()
    
    return render_template("rankings/index.html",
                                category=category,
                                year=year,
                                cols=cols,
                                years=years,
                                rankings=rankings)
