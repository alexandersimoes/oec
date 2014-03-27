import time, urllib, urllib2, json

from flask import Blueprint, render_template, g, request, session, redirect, \
                    url_for, flash, jsonify, Response, abort
from flask.ext.babel import gettext

from oec import app, db, babel, view_cache, random_countries, available_years
from oec.utils import make_query, make_cache_key
from oec.db_attr.models import Country, Sitc, Hs
from oec.explore.models import Build, App, Short
from oec.db_hs import models as hs_tbls
from oec.db_sitc import models as sitc_tbls
from sqlalchemy.sql.expression import func
from sqlalchemy import not_
from random import choice

from config import FACEBOOK_ID

mod = Blueprint('explore', __name__, url_prefix='/explore')

@mod.route('/')
@mod.route('/<app_name>/')
def explore_redirect(app_name='tree_map'):
    '''fetch random country'''
    c = Country.query.get(choice(random_countries))

    if app_name in ["tree_map", "stacked", "network"]:
        redirect_url = url_for('.explore', app_name=app_name, \
                        classification="hs", trade_flow="export", \
                        origin_id=c.id_3char, dest_id="all", prod_id="show", year="2011")
    elif app_name in ["geo_map", "rings"]:
        '''fetch random product'''
        p = Hs.query.filter(Hs.hs != None) \
                            .order_by(func.random()).limit(1).first()
        origin = "show"
        if app_name == "rings":
            origin = c.id_3char
        redirect_url = url_for('.explore', app_name=app_name, \
                        classification="hs", trade_flow="export", \
                        origin_id=origin, dest_id="all", prod_id=p.hs, year="2011")
    else:
        abort(404)
    return redirect(redirect_url)

def sanitize(app_name, classification, trade_flow, origin, dest, product, year):
    msg = None
    if origin == "twn" and dest != "all":
        c = Country.query.filter_by(id_3char=origin).first()
        origin = "chn"
        msg = "Bilateral trade not available for {0}. ".format(c.get_name())
    if classification == "hs":
        if origin in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=origin).first()
            origin = "zaf"
            msg = "{0} reports their trade under South Africa in the HS classification. ".format(c.get_name())
        if dest in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=dest).first()
            dest = "zaf"
            msg = "{0} reports their trade under South Africa in the HS classification. ".format(c.get_name())

    if msg:
        redirect_url = url_for('.explore', app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin_id=origin, dest_id=dest, prod_id=product, year=year)
        flash(msg+"<script>redirect('"+redirect_url+"', 10)</script>")

def get_origin_dest_prod(origin_id, dest_id, prod_id, classification, year, trade_flow):
    prod_tbl = Hs if classification == "hs" else Sitc
    data_tbls = hs_tbls if classification == "hs" else sitc_tbls
    year = year.split(".")[1] if "." in year else year

    origin = Country.query.filter_by(id_3char=origin_id).first()
    dest = Country.query.filter_by(id_3char=dest_id).first()
    product = prod_tbl.query.filter(getattr(prod_tbl, classification) == prod_id).first()

    defaults = {"origin":"nausa", "dest":"aschn", "hs":"010101", "sitc":"105722"}

    if not origin:
        # find the largest exporter or importer of given product
        direction = "top_exporter" if trade_flow == "export" else "top_importer"
        origin = getattr(data_tbls, "Yp").query.filter_by(year=year) \
                        .filter_by(product=product).first()
        origin = defaults["origin"] if not origin else getattr(origin, direction)
        origin = Country.query.get(origin)

    if not dest:
        if product:
            # find the largest exporter or importer of given product
            direction = "top_importer" if trade_flow == "export" else "top_exporter"
            dest = getattr(data_tbls, "Yp").query.filter_by(year=year) \
                            .filter_by(product=product).first()
            if not dest:
              dest = Country.query.get("nausa")
            else:
              dest = Country.query.get(getattr(dest, direction))
        else:
            # find the largest exporter or importer destination of given country
            direction = "top_export_dest" if trade_flow == "export" else "top_import_dest"
            dest = getattr(data_tbls, "Yo").query.filter_by(year=year) \
                            .filter_by(country=origin).first()
            dest = defaults["dest"] if not dest else getattr(dest, direction)
            if not dest:
                dest = Country.query.get("nausa")
            else:
                dest = Country.query.get(dest)

    if not product:
        # find the largest exporter or importer of given product
        direction = "top_export" if trade_flow == "export" else "top_import"
        product = getattr(data_tbls, "Yo").query.filter_by(year=year) \
                        .filter_by(country=origin).first()
        product = defaults[classification] if not product else getattr(product, direction)
        product = prod_tbl.query.get(product)

    return (origin, dest, product)


@mod.route('/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year>/')
@view_cache.cached(timeout=2592000, key_prefix=make_cache_key)
def explore(app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year="2011"):
    g.page_type = mod.name

    '''Make sure year is within bounds, if not redirect'''
    start_year = year.split(".")[0] if "." in year else year
    end_year = year.split(".")[1] if "." in year else year
    new_start_year, new_end_year = start_year, end_year
    if int(start_year) < available_years[classification][0]:
        new_start_year = str(available_years[classification][0])
        new_year = new_start_year
    if int(end_year) > available_years[classification][-1]:
        new_end_year = str(available_years[classification][-1])
        new_year = new_end_year
    if new_start_year != start_year or new_end_year != end_year:
        new_year = ".".join([new_start_year, new_end_year]) if "." in year else new_year
        return redirect(url_for('.explore', app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=new_year))

    sanitize(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year)

    '''Every possible build for accordion links'''
    all_builds = Build.query.all()
    origin, dest, prod = get_origin_dest_prod(origin_id, dest_id, prod_id, \
                                            classification, year, trade_flow)

    for i, build in enumerate(all_builds):
        build.set_options(origin=origin, dest=dest, product=prod, classification=classification, year=year)

    current_app = App.query.filter_by(type=app_name).first_or_404()
    build_filters = {"origin":origin_id,"dest":dest_id,"product":prod_id}
    for bf_name, bf in build_filters.items():
        if bf != "show" and bf != "all":
            build_filters[bf_name] = "<" + bf_name + ">"

    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow,
                        origin=build_filters["origin"], dest=build_filters["dest"],
                        product=build_filters["product"]).first_or_404()

    current_build.set_options(origin=origin, dest=dest, product=prod,
                                classification=classification, year=year)

    kwargs = {"trade_flow":trade_flow, "origin_id":origin, "dest_id":dest, "year":year}
    if classification == "sitc":
        kwargs["sitc_id"] = prod
    else:
        kwargs["hs_id"] = prod

    return render_template("explore/index.html",
        current_build = current_build,
        all_builds = all_builds)

@mod.route('/<app_name>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('/<app_name>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def explore_legacy(app_name, trade_flow, origin, dest, product, year='2011'):
    if not year.isdigit():
        abort(404)
    c = 'sitc' if int(year) < 1995 else 'hs'
    if product != "show" and product != "all":
        prod = Hs.query.filter_by(hs=product).first()
        c = 'hs'
        if not prod:
            c = 'sitc'
            prod = Sitc.query.filter_by(sitc=product).first()
        product = prod.id
    return redirect(url_for('.explore', app_name=app_name, \
                classification=c, trade_flow=trade_flow, origin=origin, \
                dest=dest, product=product, year=year))

@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def embed(app_name, classification, trade_flow, origin, dest, \
                product, year="2011"):

    current_app = App.query.filter_by(type=app_name).first_or_404()
    build_filters = {"origin":origin,"dest":dest,"product":product}
    for bf_name, bf in build_filters.items():
        if bf != "show" and bf != "all":
            build_filters[bf_name] = "<" + bf_name + ">"

    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow,
                        origin=build_filters["origin"], dest=build_filters["dest"],
                        product=build_filters["product"]).first_or_404()
    current_build.set_options(origin=origin, dest=dest, product=product,
                                classification=classification, year=year)

    '''Get URL query parameters from reqest.args object to return to the view.
    '''
    global_vars = {x[0]:x[1] for x in request.args.items()}
    if "controls" not in global_vars:
        global_vars["controls"] = "true"
    
    return render_template("explore/embed.html",
        current_build = current_build,
        global_vars = json.dumps(global_vars),
        facebook_id = FACEBOOK_ID)

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
    import tempfile, subprocess

    data = request.form["content"]
    format = request.form["format"]
    title = request.form["title"]

    temp = tempfile.NamedTemporaryFile()
    temp.write(data.encode("utf-8"))
    temp.seek(0)

    if format == "png":
        mimetype='image/png'
    elif format == "pdf":
        mimetype='application/pdf'
    elif format == "svg":
        mimetype='application/octet-stream'
    elif format == "csv":
        mimetype="text/csv;charset=UTF-8"

    if format == "png" or format == "pdf":
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        response_data = out
    else:
        response_data = data.encode("utf-8")

    content_disposition = "attachment;filename=%s.%s" % (title, format)
    content_disposition = content_disposition.replace(",", "_")

    return Response(response_data,
                        mimetype=mimetype,
                        headers={"Content-Disposition": content_disposition})
