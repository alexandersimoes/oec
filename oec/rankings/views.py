# -*- coding: utf-8 -*-
import time, urllib2, json

from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, Response
from flask.ext.babel import gettext

from oec import app, db, babel, view_cache, available_years
from oec.utils import make_cache_key, compile_query
from oec.db_attr.models import Yo, Sitc, Sitc_name, Country, Country_name
from oec.db_attr.models import Hs92, Hs92_name, Hs96, Hs96_name, Hs02, Hs02_name, Hs07, Hs07_name
# from oec.db_hs.models import Yp as Yp_hs
# from oec.db_sitc.models import Yp as Yp_sitc
from oec import db_data
from oec.general.views import get_locale
import csv
from cStringIO import StringIO
from oec import utils

@app.route('/rankings/')
@app.route('/rankings/<any("country","sitc","hs","hs92","hs96","hs02","hs07"):category>/')
@app.route('/rankings/<any("country","sitc","hs","hs92","hs96","hs02","hs07"):category>/<int:year>/')
def rankings_redirect_nolang(category=None, year=None):
    if category:
        redirect_url = url_for('rankings.rankings', lang=g.locale, category=category, year=year)
    else:
        redirect_url = url_for('rankings.rankings_redirect', lang=g.locale)
    return redirect(redirect_url)

mod = Blueprint('rankings', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","vi","zh"):lang>/rankings')

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.route('/')
def rankings_redirect():
    return redirect(url_for('.rankings', lang=g.locale, category="country"))

@mod.route('/<any("country","sitc","hs","hs92","hs96","hs02","hs07"):category>/')
@mod.route('/<any("country","sitc","hs","hs92","hs96","hs02","hs07"):category>/<int:year>/')
# don't cache because downloading will not be possible
# @view_cache.cached(timeout=2592000, key_prefix=make_cache_key)
def rankings(category=None, year=None):
    category = "hs92" if category == "hs" else category
    if category == "country":
        g.page_sub_type = "countries"
    else:
        g.page_sub_type = "products"
    try:
        depth = int(request.args.get('depth', 4))
    except:
        depth = 4
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
        return redirect(url_for('.rankings', lang=g.locale, category=category, year=available_years[category][0]))
    elif year < available_years[category][0]:
        return redirect(url_for('.rankings', lang=g.locale, category=category, year=available_years[category][-1]))

    # if category == "sitc":
    #     Yp = getattr(db_data, "sitc_models").Yp
    #     Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Sitc, Sitc_name, Yp, "sitc_id", "pci", "pci_rank", "pci_rank_delta"]
    #     cols = [gettext("Rank"), "", "SITC", gettext("Product"), "PCI Value"]
    #
    # elif category == "hs":
    #     Yp = getattr(db_data, "hs92_models").Yp
    #     Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Hs, Hs_name, Yp, "hs_id", "pci", "pci_rank", "pci_rank_delta"]
    #     cols = [gettext("Rank"), "", "HS", gettext("Product"), "PCI Value"]
    
    cols = [{"id":"rank", "name":gettext("Rank"),"sortable":True}, 
            {"id":"delta", "name":"","sortable":False}, 
            {"id":"id", "name":gettext("ID"),"sortable":True, "sort-alpha":True}]
    if category == "country":
        Attr, Attr_name, Attr_data, attr_id, index, rank, delta = [Country, Country_name, Yo, "origin_id", "eci", "eci_rank", "eci_rank_delta"]
        cols += [{"id":"country", "name":gettext("Country"), "sortable":True, "sort-alpha":True}, {"id":"eci", "name":"ECI", "sortable":True}]
    else:
        Attr_data = getattr(db_data, "{}_models".format(category)).Yp
        Attr = globals()[category.title()]
        Attr_name = globals()["{}_name".format(category.title())]
        attr_id = "{}_id".format(category)
        index, rank, delta = ["pci", "pci_rank", "pci_rank_delta"]
        cols += [{"id":"product", "name":gettext("Product"), "sortable":True, "sort-alpha":True}, {"id":"pci", "name":"PCI", "sortable":True}]


    rankings = db.session.query(Attr, Attr_name, Attr_data) \
                .filter(getattr(Attr_name, attr_id) == Attr.id) \
                .filter(getattr(Attr_data, attr_id) == Attr.id) \
                .filter(Attr_name.lang == g.locale) \
                .filter(getattr(Attr_data, index) != None)

    if category != "country":
        x = depth+2
        x = "{}".format(x)
        rankings = rankings.filter(getattr(Attr_data, "{}_id_len".format(category)) == x)

    if download_all:
        title = "{0}_all_ranking_{1}".format(category, g.locale)
        rankings = rankings.order_by(Attr_data.year).order_by(getattr(Attr_data, rank))
    else:
        title = "{0}_{1}_ranking_{2}".format(category, year, g.locale)
        rankings = rankings.filter(Attr_data.year == year).order_by(getattr(Attr_data, rank))

    # raise Exception(utils.compile_query(rankings))
    rankings = rankings.all()

    if download:
        cols = [{"id":"year", "name":gettext("Year")}] + cols
        writer.writerow(filter(None, [unicode(c["name"]).encode("utf-8") for c in cols]))
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
                                depth=depth,
                                cols=cols,
                                years=available_years[category][::-1],
                                rankings=rankings)
