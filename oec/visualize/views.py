import os, time, urllib, urllib2, json, csv, io
import tempfile, subprocess
from werkzeug.routing import ValidationError, BaseConverter
from flask import Blueprint, render_template, g, request, session, redirect, \
                    url_for, flash, jsonify, Response, abort, make_response
from flask.ext.babel import gettext

from oec import app, db, babel, view_cache, random_countries, available_years, oec_dir
from oec.utils import make_query, make_cache_key, compile_query
from oec.db_attr.models import Country, Sitc, Hs92, Hs96, Hs02, Hs07
# from oec.db_hs import models as hs_tbls
# from oec.db_sitc import models as sitc_tbls
from oec import db_data, db_attr
from oec.general.views import get_locale
from oec.visualize.models import Build, get_all_builds, Short
from sqlalchemy.sql.expression import func
from sqlalchemy import not_, desc
from random import choice
from config import FACEBOOK_ID

mod = Blueprint('visualize', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","vi","zh"):lang>/visualize')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.route('/')
@mod.route('/<app_name>/')
def visualize_redirect(app_name='tree_map'):
    '''fetch random country'''
    c = Country.query.get(choice(random_countries))
    latest_hs_year = [available_years['hs92'][-1]]

    if app_name in ["tree_map", "stacked", "network"]:
        year = [available_years['hs92'][0], available_years['hs92'][-1]] if app_name == "stacked" else latest_hs_year
        redirect_url = url_for('.visualize', lang=g.locale, app_name=app_name, \
                        classification="hs92", trade_flow="export", \
                        origin_id=c.id_3char, dest_id="all", prod_id="show", year=year)
    elif app_name in ["geo_map", "rings"]:
        '''fetch random product'''
        p = Hs92.query.filter(Hs92.hs92 != None).filter(func.length(Hs92.hs92) == 4) \
                            .order_by(func.random()).limit(1).first()
        origin = "show"
        if app_name == "rings":
            origin = c.id_3char
        redirect_url = url_for('.visualize', lang=g.locale, app_name=app_name, \
                        classification="hs92", trade_flow="export", \
                        origin_id=origin, dest_id="all", prod_id=p.hs92, year=latest_hs_year)
    elif app_name in ["scatter"]:
        redirect_url = url_for('.visualize', lang=g.locale, app_name=app_name, \
                        classification="hs92", trade_flow="gdp", \
                        origin_id="show", dest_id="all", prod_id="all", year=latest_hs_year)
    else:
        abort(404)
    return redirect(redirect_url)

def sanitize(app_name, classification, trade_flow, origin, dest, product, year):
    msg = None
    classifications = ['sitc', 'hs92', 'hs96', 'hs02', 'hs07']

    '''Check classification'''
    # support for legacy URLs that use hs not hs92
    if classification not in classifications:
        classification = 'hs92'
        msg = u"Data only available in the following classification: SITC, HS92, HS96, HS02, HS07"
    elif not set(year).issubset(set(available_years[classification])):
        found = False
        for c in reversed(classifications):
            if set(year).issubset(set(available_years[c])):
                classification = c
                found = True
                break
        if not found:
            classification = 'hs92'
            year = [available_years[classification][-1]] if len(year) == 1 else available_years[classification]
        msg = u"Classification changed to {} for the data requested.".format(classification)
    '''Check countries:'''
    if origin == "twn" and dest != "all":
        c = Country.query.filter_by(id_3char=origin).first()
        origin = "chn"
        msg = u"Bilateral trade not available for {}. ".format(c.get_name())
    if "hs" in classification:
        if origin in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=origin).first()
            origin = "zaf"
            msg = u"{} reports their trade under South Africa in the HS classification. ".format(c.get_name())
        if dest in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=dest).first()
            dest = "zaf"
            msg = u"{} reports their trade under South Africa in the HS classification. ".format(c.get_name())
        if origin in ["bel", "lux"]:
            c = Country.query.filter_by(id_3char=origin).first()
            origin = "blx"
            msg = u"{} reports their trade under Belgium-Luxembourg in the HS classification. ".format(c.get_name())
        if dest in ["bel", "lux"]:
            c = Country.query.filter_by(id_3char=dest).first()
            dest = "blx"
            msg = u"{} reports their trade under Belgium-Luxembourg in the HS classification. ".format(c.get_name())
    '''Check that stacked has given year range'''
    if app_name in ["stacked", "line"] and len(year) < 2:
        msg = "Need to specify a range of years"
        year = [available_years[classification][0], available_years[classification][-1]]
    '''Check that scatter is in acceptable year range 1980+'''
    if app_name == "scatter" and not year:
        msg = "GDP data only available from 1980 onwards. "
        year = [1980]

    if msg:
        redirect_url = url_for('.visualize', lang=g.locale, app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin_id=origin, dest_id=dest, prod_id=product, year=year)
        return [msg, redirect_url]


def get_origin_dest_prod(origin_id, dest_id, prod_id, classification, year, trade_flow):
    prod_tbl = getattr(db_attr.models, classification.capitalize())
    data_tbls = getattr(db_data, "{}_models".format(classification))

    origin = Country.query.filter_by(id_3char=origin_id).first() if origin_id else origin_id
    dest = Country.query.filter_by(id_3char=dest_id).first() if dest_id else dest_id
    product = prod_tbl.query.filter(getattr(prod_tbl, classification) == prod_id).first()

    defaults = {"origin":"nausa", "dest":"aschn", "hs92":"010101", "hs96":"010101", "hs02":"010101", "hs07":"010101", "sitc":"105722"}

    if not origin:
        if dest:
            origin = getattr(data_tbls, "Yod").query \
                .filter_by(year=year[-1]) \
                .filter_by(dest=dest) \
                .order_by(desc("export_val")).first()
            origin = origin.origin if origin else defaults["origin"]
        else:
            # find the largest exporter or importer of given product
            direction = "top_exporter" if trade_flow == "export" else "top_importer"
            origin = getattr(data_tbls, "Yp").query.filter_by(year=year[-1]) \
                            .filter_by(product=product).first()
            origin = defaults["origin"] if not origin else getattr(origin, direction)
            origin = Country.query.get(origin)

    if not dest:
        if product:
            # find the largest exporter or importer of given product
            direction = "top_importer" if trade_flow == "export" else "top_exporter"
            dest = getattr(data_tbls, "Yp").query.filter_by(year=year[-1]) \
                            .filter_by(product=product).first()
            if not dest:
              dest = Country.query.get(defaults["dest"])
            else:
              dest = Country.query.get(getattr(dest, direction))
        else:
            # find the largest exporter or importer destination of given country
            direction = "top_export_dest" if trade_flow == "export" else "top_import_dest"
            dest = getattr(data_tbls, "Yo").query.filter_by(year=year[-1]) \
                            .filter_by(country=origin).first()
            dest = defaults["dest"] if not dest else getattr(dest, direction)
            if not dest:
                dest = Country.query.get(defaults["dest"])
            else:
                dest = Country.query.get(dest)

    if not product:
        # find the largest exporter or importer of given product
        tf = trade_flow if trade_flow in ["export", "import"] else "export"
        direction = "top_{}".format(tf) if classification == "sitc" else "top_{}_hs4".format(tf)
        product = getattr(data_tbls, "Yo").query.filter_by(year=year[-1]) \
                        .filter_by(country=origin).first()
        if product and getattr(product, direction):
            product = getattr(product, direction)
        else:
            product = defaults[classification]

    return (origin, dest, product)

'''
    Using a terminal, this view can be tested via:
    curl -d url=/en/visualize/embed/stacked/hs/export/gbr/all/show/2002.2012/?lang=en http://localhost:5000/en/visualize/shorten/
'''
@mod.route('/shorten/', methods=['GET', 'POST'])
def shorten_url():

    if request.method == 'POST':

        long_url = urllib.unquote(request.form["url"].encode('utf-8')).decode("utf-8")

        short = Short.query.filter_by(long_url = long_url).first()
        if short is None:
            slug = Short.make_unique_slug(long_url)
            short = Short(slug = slug, long_url = long_url)
            db.session.add(short)
            db.session.commit()

        return jsonify({"slug": short.slug})

    return jsonify({"error": "No URL given."})

@mod.route('/download/', methods=['GET', 'POST'])
def download():
    data = request.form.get("content", None) or request.json.get("content", None)
    format = request.form.get("format", None) or request.json.get("format", None)
    title = request.form.get("title", None) or request.json.get("title", None)
    title = "{0}_{1}".format(g.locale, title)
    save = request.json.get("save", False) if request.json else None

    if save:
        file_path = os.path.abspath(os.path.join(oec_dir, 'static/generated', "{0}.png".format(title)))
        if os.path.isfile(file_path):
            return jsonify({"file_name":"{0}.png".format(title), "new":False})
        new_file = open(file_path, 'w')

    if format == "png":
        mimetype='image/png'
    elif format == "pdf":
        mimetype='application/pdf'
    elif format == "svg":
        mimetype='application/octet-stream'
    elif format == "csv":
        mimetype="text/csv;charset=UTF-8"

    if format == "png" or format == "pdf":
        temp = tempfile.NamedTemporaryFile()
        temp.write(data.encode("utf-8"))
        temp.seek(0)
        zoom = "1"
        background = "#ffffff"
        if save:
            p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "-o", file_path, "--background-color={0}".format(background), temp.name])
            out, err = p.communicate()
        else:
            p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
            out, err = p.communicate()
            response_data = out
    elif format == "csv":
        output = io.BytesIO()
        response_data = json.loads(data.encode("utf-8"))
        writer = csv.writer(output)
        writer.writerows(response_data)
        response_data = output.getvalue()
    else:
        response_data = data.encode("utf-8")

    if save:
        return jsonify({"file_name":os.path.basename(new_file.name), "new":True})

    content_disposition = "attachment;filename=%s.%s" % (title, format)
    content_disposition = content_disposition.replace(",", "_")

    return Response(response_data,
                        mimetype=mimetype,
                        headers={"Content-Disposition": content_disposition})

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
# @view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def visualize(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year=None):
    g.page_type = "visualize"
    g.page_sub_type = app_name

    if app_name == "scatter":
        year = [y for y in year if y >= 1980]
    elif trade_flow == "eci":
        year = [y for y in year if y >= 1964]

    '''sanitize input args'''
    redir = sanitize(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year)
    if redir:
        flash(redir[0])
        return redirect(redir[1])

    '''get this build'''
    build = Build(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year)
    if build.title() is None and build.question() is None:
        abort(404)

    '''get every possible build for sub nav'''
    origin, dest, prod = get_origin_dest_prod(origin_id, dest_id, prod_id, classification, year, trade_flow)
    all_builds = get_all_builds(classification, origin_id, dest_id, prod_id, year, {"origin":origin, "dest":dest, "prod":prod})

    '''create the ui array for the current build'''
    ui = []

    all_country = {
        "color": "#333333",
        "display_id": "all",
        "id": "all",
        "icon": "/static/img/icons/app/app_geo_map.png",
        "name": "All"
    }
    all_placed = False

    if build.trade_flow != "eci" and build.viz["slug"] not in ("scatter", "geo_map") and build.origin != "show":
        if isinstance(build.origin, Country):
            origin_country = build.origin.serialize()
        else:
            origin_country = all_country
            all_placed = True

        ui.append({
            "id": "origin",
            "name": gettext("Country"),
            "data": [origin_country],
            "url": url_for('attr.attrs', attr='country', lang=g.locale)
        })

    dest_country = False
    prod_exists = isinstance(build.prod, (Sitc, Hs92, Hs96, Hs02, Hs07))

    if isinstance(build.dest, Country):
        dest_country = build.dest.serialize()
    elif not all_placed and not prod_exists and build.viz["slug"] in ("tree_map", "line", "stacked"):
        dest_country = all_country

    if dest_country:
        ui.append({
            "id": "destination",
            "name": gettext("Country") if build.trade_flow == "eci" else gettext("Partner"),
            "data": [dest_country],
            "url": url_for('attr.attrs', attr='country', lang=g.locale)
        })

    if prod_exists:
        product = {
            "id": "product",
            "name": gettext("Product"),
            "data": [build.prod.serialize()],
            "url": url_for('attr.attrs', attr=build.classification, lang=g.locale)
        }
        ui.append(product)

    if build.viz["slug"] == "scatter":
        trade_flow = {
            "id": "trade_flow",
            "name": gettext("Y Axis"),
            "current": build.trade_flow,
            "data": [
                {"name": gettext("GDP"), "display_id":"gdp"},
                {"name": gettext("GDPpc (constant '05 US$)"), "display_id":"gdp_pc_constant"},
                {"name": gettext("GDPpc (current US$)"), "display_id":"gdp_pc_current"},
                {"name": gettext("GDPpc PPP (constant '11)"), "display_id":"gdp_pc_constant_ppp"},
                {"name": gettext("GDPpc PPP (current)"), "display_id":"gdp_pc_current_ppp"}
            ]
        }
    else:
        trade_flow = {
            "id": "trade_flow",
            "name": gettext("Trade Flow"),
            "current": build.trade_flow,
            "data": [
                {"name": gettext("Export"), "display_id":"export"},
                {"name": gettext("Import"), "display_id":"import"}
            ]
        }

    if build.trade_flow not in ("show", "eci"):
        ui.append(trade_flow)

    if build.trade_flow != "eci":
        ui.append({
            "id": "classification",
            "name": gettext("Dataset"),
            "current": build.classification,
            "data": ["HS92", "HS96", "HS02", "HS07", "SITC"]
        })

    years = set()
    for d in available_years:
        [years.add(y) for y in available_years[d] if (build.trade_flow == "eci" and y >= 1964) or (build.viz["slug"] == "scatter" and y >= 1980) or (build.viz["slug"] != "scatter" and build.trade_flow != "eci")]

    if build.viz["slug"] in ("stacked", "line"):
        ui.append({
            "id": "start_year",
            "name": gettext("Start Year"),
            "current": build.year[0],
            "data": years
        })
        ui.append({
            "id": "end_year",
            "name": gettext("End Year"),
            "current": build.year[-1],
            "data": years
        })
    else:
        ui.append({
            "id": "year",
            "name": gettext("Year"),
            "current": build.year[-1],
            "data": years
        })

    builds_by_app = {}
    for b in all_builds:
        if b.viz["slug"] not in ("stacked", "line"):
            b.year = [b.year[-1]]
            b.year_str = Build.year_to_str(b, b.year)
        if not hasattr(builds_by_app, b.viz["slug"]):
            builds_by_app[b.viz["slug"]] = []
    for b in all_builds:
        builds_by_app[b.viz["slug"]].append(b)

    page = "index_new" if request.args.get("beta") == "" else "index"

    return render_template("visualize/{}.html".format(page),
        current_build = build, build_ui = ui,
        all_builds = builds_by_app.values())

@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def embed(app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year=available_years['hs92'][-1]):

    g.page_type = "embed"
    '''support for legacy URLs that use hs not hs92'''
    if classification not in ['sitc', 'hs92', 'hs96', 'hs02', 'hs07']:
        return redirect(url_for('.embed', lang=g.locale, app_name=app_name, \
                        classification='hs92', trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year))

    b = Build(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year)

    '''Get URL query parameters from reqest.args object to return to the view.
    '''
    global_vars = {x[0]:x[1] for x in request.args.items()}
    if "controls" not in global_vars:
        global_vars["controls"] = "true"

    return render_template("visualize/embed.html",
        build = b,
        global_vars = json.dumps(global_vars),
        facebook_id = FACEBOOK_ID)

@mod.route('/builds/')
def builds():
    focus = request.args.get('focus')
    build_args = {}
    build_args["classification"] = request.args.get('classification', 'hs92')
    build_args["origin_id"] = request.args.get('origin_id') or request.args.get('dest_id')
    build_args["dest_id"] = request.args.get('dest_id') or None
    build_args["prod_id"] = request.args.get('prod_id') or None
    build_args["year"] = request.args.get('year', available_years[build_args["classification"]][-1])
    build_args["defaults"] = {"origin":"nausa", "dest":"aschn", "prod":"010101"}
    build_args["viz"] = ["tree_map", "rings"]
    
    if build_args["origin_id"] == build_args["dest_id"]:
        origin_dest_prod = get_origin_dest_prod(None, build_args["dest_id"], build_args["prod_id"], build_args["classification"], [build_args["year"]], "export")
        build_args["dest_id"] = origin_dest_prod[0].id_3char
    
    all_builds = get_all_builds(**build_args)
    
    if build_args["origin_id"] and build_args["dest_id"]:
        build_args["origin_id"], build_args["dest_id"] = build_args["dest_id"], build_args["origin_id"]
        all_builds = get_all_builds(**build_args) + all_builds
    
    '''
        Need some way of ranking these build...
    '''
    for build in all_builds:
        build.relevance = 0
        for var in ["trade_flow", "origin_id", "dest_id", "prod_id"]:
            build_arg_var = build_args.get(var) or request.args.get(var)
            build_var = getattr(build, var.replace("_id", ""))
            if hasattr(build_var, "get_display_id"):
                if build_var.get_display_id() == build_arg_var:
                    build.relevance += 2
            else:
                if build_arg_var == build_var:
                    build.relevance += 1
    all_builds.sort(key=lambda x: x.relevance, reverse=True)
    # raise Exception(all_builds[0])


    if focus == "origin_id":
        attr = Country.query.filter_by(id_3char=build_args["origin_id"]).first() or Country.query.filter(Country.id.endswith(build_args["origin_id"])).first()
    elif focus == "dest_id":
        attr = Country.query.filter_by(id_3char=build_args["dest_id"]).first() or Country.query.filter(Country.id.endswith(build_args["dest_id"])).first()
    elif focus == "prod_id":
        tbl = globals()[build_args["classification"].title()]
        c = build_args["classification"]
        attr = tbl.query.filter(getattr(tbl,c)==build_args["prod_id"]).first()
    attr_name = attr.get_name()
    profile = {
        "title":gettext("Profile for %(attr)s", attr=attr_name),
        "url":attr.get_profile_url(),
        "icon":attr.get_icon(),
        "color":attr.color,
        "name":attr_name
    }

    return jsonify(profile=profile, builds=[{"title": b.question(), "url": b.url(), "viz": b.viz["slug"]} for b in all_builds])
