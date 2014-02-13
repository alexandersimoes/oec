# -*- coding: utf-8 -*-
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
# don't cache because downloading will not be possible
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
        Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Sitc, Sitc_name, Yp_sitc, "sitc_id", "pci", "pci_rank", "pci_rank_delta"]
        cols = [gettext("Rank"), gettext("Rank")+u" ∆", "SITC", gettext("Product"), "PCI Value"]
    
    elif category == "hs":
        Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Hs, Hs_name, Yp_hs, "hs_id", "pci", "pci_rank", "pci_rank_delta"]
        cols = [gettext("Rank"), gettext("Rank")+u" ∆", "HS", gettext("Product"), "PCI Value"]
    
    elif category == "country":
        Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Country, Country_name, Yo, "origin_id", "eci", "eci_rank", "eci_rank_delta"]
        cols = [gettext("Rank"), gettext("Rank")+u" ∆", "Abbrv", gettext("Country"), "ECI Value"]
    
    rankings = db.session.query(Attr, Attr_name, Attr_data) \
                .filter(getattr(Attr_name, attr_id) == Attr.id) \
                .filter(getattr(Attr_data, attr_id) == Attr.id) \
                .filter(Attr_name.lang == g.locale) \
                .filter(getattr(Attr_data, index) != None)
    
    if download_all:
        title = "{0}_all_ranking_{1}".format(category, g.locale)
        rankings = rankings.order_by(Attr_data.year).order_by(getattr(Attr_data, rank))
    else:
        title = "{0}_{1}_ranking_{2}".format(category, year, g.locale)
        rankings = rankings.filter(Attr_data.year == year).order_by(getattr(Attr_data, rank))
    
    rankings = rankings.all()
    
    if download:
        cols = [gettext("Year")] + cols
        writer.writerow([unicode(c).encode("utf-8") for c in cols])
        for r in rankings:
            writer.writerow([r[2].year, \
                                getattr(r[2], rank), \
                                r[0].get_display_id(), \
                                unicode(r[1].name).encode("utf-8"), \
                                getattr(r[2], index)])
        content_disposition = "attachment;filename={0}.csv".format(title)
        content_disposition = content_disposition.replace(",", "_")
        return Response(s.getvalue(), 
                            mimetype="text/csv;charset=UTF-8", 
                            headers={"Content-Disposition": content_disposition})
    
    else:
        return render_template("rankings/index.html",
                                category=category,
                                year=year,
                                cols=cols,
                                years=available_years[category][::-1],
                                rankings=rankings)
