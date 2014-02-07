import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, Response
from flask.ext.babel import gettext

from oec import app, db, babel, view_cache, available_years
from oec.utils import make_cache_key, compile_query
from oec.db_attr.models import Yo, Hs, Hs_name, Sitc, Sitc_name, Country, Country_name
from oec.db_hs.models import Yp as Yp_hs
from oec.db_sitc.models import Yp as Yp_sitc

import csv
from cStringIO import StringIO

mod = Blueprint('rankings', __name__, url_prefix='/rankings')

@mod.route('/')
def rankings_redirect():
    return redirect(url_for('.rankings', category="country"))

@mod.route('/<category>/')
@mod.route('/<category>/<int:year>/')
# @view_cache.cached(timeout=2592000, key_prefix=make_cache_key)
def rankings(category=None,year=None):    
    g.page_type = mod.name
    
    download = request.args.get('download', None)
    download_all = False
    if download:
        s = StringIO()
        writer = csv.writer(s)
    
    if category == None:
        category = "country"
    
    if year == None:
        download_all = True if download else False
        year = available_years[category][-1]
    elif year > available_years[category][-1]:
        return redirect(url_for('.rankings', category=category, year=available_years[category][0]))
    elif year < available_years[category][0]:
        return redirect(url_for('.rankings', category=category, year=available_years[category][-1]))
    
    if category == "sitc":
        cols = [gettext("Rank"), "SITC", gettext("Product"), "PCI Value"]
        rankings = db.session.query(Sitc, Sitc_name, Yp_sitc) \
                    .filter(Sitc_name.sitc_id == Sitc.id) \
                    .filter(Yp_sitc.sitc_id == Sitc.id) \
                    .filter(Sitc_name.lang == g.locale) \
                    .filter(Yp_sitc.pci != None) \
                    .order_by(Yp_sitc.pci_rank)
        if not download_all:
            rankings = rankings.filter(Yp_sitc.year == year)
        rankings = rankings.all()
        if download:
            writer.writerow([unicode(c).encode("utf-8") for c in cols])
            for r in rankings:
                writer.writerow([r[2].pci_rank, r[0].get_display_id(), unicode(r[1].name).encode("utf-8"), r[2].pci])
    
    elif category == "hs":
        cols = [gettext("Rank"), "HS", gettext("Product"), "PCI Value"]
        rankings = db.session.query(Hs, Hs_name, Yp_hs) \
                    .filter(Hs_name.hs_id == Hs.id) \
                    .filter(Yp_hs.hs_id == Hs.id) \
                    .filter(Yp_hs.year == year) \
                    .filter(Hs_name.lang == g.locale) \
                    .filter(Yp_hs.pci != None) \
                    .order_by(Yp_hs.pci_rank).all()
        if download:
            writer.writerow([unicode(c).encode("utf-8") for c in cols])
            for r in rankings:
                writer.writerow([r[2].pci_rank, r[0].get_display_id(), unicode(r[1].name).encode("utf-8"), r[2].pci])
    
    elif category == "country":
        cols = [gettext("Rank"), "Abbrv", gettext("Country"), "ECI Value"]
        rankings = db.session.query(Country, Country_name, Yo) \
                    .filter(Country_name.country_id == Country.id) \
                    .filter(Yo.origin_id == Country.id) \
                    .filter(Yo.year == year) \
                    .filter(Country_name.lang == g.locale) \
                    .filter(Yo.eci != None) \
                    .order_by(Yo.eci_rank).all()
        if download:
            writer.writerow([unicode(c).encode("utf-8") for c in cols])
            for r in rankings:
                writer.writerow([r[2].eci_rank, r[0].get_display_id(), unicode(r[1].name).encode("utf-8"), r[2].eci])
    
    if download:    
        content_disposition = "attachment;filename={0}_{1}_ranking.csv".format(category, year)
        content_disposition = content_disposition.replace(",", "_")
        return Response(s.getvalue(), 
                            mimetype="text/csv;charset=UTF-8", 
                            headers={"Content-Disposition": content_disposition})
    
    else:
        return render_template("rankings/index.html",
                                category=category,
                                year=year,
                                cols=cols,
                                years=available_years[category],
                                rankings=rankings)
