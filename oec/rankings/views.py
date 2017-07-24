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
    return redirect(url_for('.rankings', lang=g.locale, attr="country"))

@mod.route('/<any("sitc","hs","hs92","hs96","hs02","hs07"):category>/')
@mod.route('/<any("country","sitc","hs","hs92","hs96","hs02","hs07"):category>/<int:year>/')
def rankings_legacy(category=None, year=None):
    category = "hs92" if category == "hs" else category
    if category in ["sitc", "hs", "hs92", "hs96", "hs02", "hs07"]:
        classification = category
        category = "product"
    else:
        classification = "hs92"
    try:
        depth = int(request.args.get('depth', 4))
    except:
        depth = 4
    return redirect(url_for('.rankings', lang=g.locale, attr=category, classification=classification))

@mod.route('/<any("country","product"):attr>/')
@mod.route('/<any("product"):attr>/<any("sitc","hs92","hs96","hs02","hs07"):classification>/')
@mod.route('/<any("country"):attr>/<any("neci","eci"):complexity_type>/')
# don't cache because downloading will not be possible
# @view_cache.cached(timeout=2592000, key_prefix=make_cache_key)
def rankings(attr=None, classification="sitc", complexity_type="pci"):
    year_ranges = {
        "sitc": ["1966-1970","1971-1975","1976-1980","1981-1985","1986-1990","1991-1995","1996-2000","2001-2005","2006-2010","2011-2015"],
        "hs92": ["1995-2000","2001-2005","2006-2010","2011-2015"],
        "hs96": ["1998-2000","2001-2005","2006-2010","2011-2015"],
        "hs02": ["2003-2005","2006-2010","2011-2015"],
        "hs07": ["2008-2010","2011-2015"]
    }
    year = None
    year_range = request.args.get('year_range', year_ranges[classification][-1])
    year_range = year_range if year_range in year_ranges[classification] else year_ranges[classification][-1]
    g.page_sub_type = "countries"
    depth = 4

    download = bool(request.args.get('download', None))
    download_all = bool(request.args.get('download_all', None))
    if download:
        s = StringIO()
        writer = csv.writer(s)

    cols = []
    if attr == "country":
        Attr, Attr_name, Attr_data, attr_id = [Country, Country_name, Yo, "origin_id"]
        cols += [{"id":"country", "name":gettext("Country"), "sortable":True, "sort-alpha":True}, {"id":complexity_type, "name":"ECI", "sortable":True}]
    else:
        Attr_data = getattr(db_data, "{}_models".format(classification)).Yp
        Attr = globals()[classification.title()]
        Attr_name = globals()["{}_name".format(classification.title())]
        attr_id = "{}_id".format(classification)
        cols += [{"id":"product", "name":gettext("Product"), "sortable":True, "sort-alpha":True}, {"id":"pci", "name":"PCI", "sortable":True}]


    '''
    rankings = db.session.query(Attr, Attr_name, Attr_data) \
                .filter(getattr(Attr_name, attr_id) == Attr.id) \
                .filter(getattr(Attr_data, attr_id) == Attr.id) \
                .filter(Attr_name.lang == g.locale) \
                .filter(getattr(Attr_data, complexity_type) != None)

    if category != "country":
        x = depth+2
        x = "{}".format(x)
        rankings = rankings.filter(getattr(Attr_data, "{}_id_len".format(category)) == x)

    if download_all:
        title = "{0}_all_ranking_{1}".format(category, g.locale)
        rankings = rankings.order_by(Attr_data.year).order_by(getattr(Attr_data, rank))
    else:
        title = "{0}_{1}_ranking_{2}".format(category, year, g.locale)
        rankings = rankings.filter(Attr_data.year >= year-10).order_by(getattr(Attr_data, rank))
    '''
    eci_date_range = map(int, year_range.split('-'))
    eci_date_range = range(eci_date_range[0], eci_date_range[1]+1)
    # rankings = Attr_data.query.filter(getattr(Attr_data, complexity_type) != None).filter(Attr_data.year >= year-10)
    rankings = db.session.query(Attr_name, Attr_data) \
                .filter(getattr(Attr_name, attr_id) == getattr(Attr_data, attr_id)) \
                .filter(Attr_name.lang == g.locale) \
                .filter(getattr(Attr_data, complexity_type) != None)

    # filter query by year range IF we're not downloading all years
    if not download_all:
        rankings = rankings.filter(Attr_data.year >= eci_date_range[0]).filter(Attr_data.year <= eci_date_range[-1])

    # raise Exception(utils.compile_query(rankings))
    rankings = rankings.all()

    if download:
        if attr == "country":
            if download_all:
                title = "eci_country_rankings"
            else:
                title = "eci_country_rankings_{}_{}".format(eci_date_range[0], eci_date_range[-1])
            cols = [{"id":"year", "name":"Year"}, {"id":"country", "name":"Country"}, {"id":"country_id", "name":"Country ID"}, {"id":"eci", "name":"ECI"}, {"id":"neci", "name":"ECI+"}]
        else:
            if download_all:
                title = "pci_{}_rankings".format(classification)
            else:
                title = "pci_{}_rankings_{}_{}".format(classification, eci_date_range[0], eci_date_range[-1])
            cols = [{"id":"year", "name":"Year"}, {"id":"product", "name":"Product"}, {"id":"product_id", "name":"{} ID".format(classification.capitalize())}, {"id":"pci", "name":"PCI"}]
        # raise Exception(filter(None, [unicode(c["name"]).encode("utf-8") for c in cols]))
        writer.writerow(filter(None, [unicode(c["name"]).encode("utf-8") for c in cols]))
        for r in rankings:
            if attr == "country":
                writer.writerow([r[1].year, unicode(r[0].name).encode("utf-8"), r[0].id, r[1].eci, r[1].neci])
            else:
                writer.writerow([r[1].year, unicode(r[0].name).encode("utf-8"), r[0].id, r[1].pci])
        content_disposition = "attachment;filename={}.csv".format(title)
        content_disposition = content_disposition.replace(",", "_")
        return Response(s.getvalue(),
                            mimetype="text/csv;charset=UTF-8",
                            headers={"Content-Disposition": content_disposition})


    ranks = {}
    for r in rankings:
        item_id = getattr(r[1], attr_id)
        complexity_val = getattr(r[1], complexity_type)
        if item_id not in ranks:
            ranks[item_id] = {"id": r[0].id}
            ranks[item_id][attr] = r[0].name
        ranks[item_id]["{}_{}".format(complexity_type, r[1].year)] = complexity_val
    rankings = sorted(ranks.values(), key=lambda k: k.get("{}_{}".format(complexity_type, eci_date_range[-1])), reverse=True)

    for r in rankings:
        r["data-array"] = json.dumps([r.get("{}_{}".format(complexity_type, y)) for y in eci_date_range])
    cols = [{"id":attr, "name":gettext(attr.capitalize()), "sortable":True, "sort-alpha":True}]
    cols += [{"id":"{}_{}".format(complexity_type, y), "name":"{}".format(y), "sortable":True} for y in eci_date_range]
    cols += [{"id":"sparkline-col", "name":"", "sortable":False}]

    # raise Exception(rankings[0])
    product_stem = "hs" if "hs" in classification else "sitc"
    return render_template("rankings/index.html",
                            complexity_type=complexity_type,
                            product_stem=product_stem,
                            showing=attr,
                            category=attr,
                            classification=classification,
                            year=year,
                            depth=depth,
                            cols=cols,
                            years=available_years[classification][::-1],
                            year_ranges=year_ranges[classification],
                            year_range=year_range,
                            rankings=rankings)
