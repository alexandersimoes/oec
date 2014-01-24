import time, urllib, urllib2, json

from flask import Blueprint, render_template, g, request, session, redirect, \
                    url_for, flash, jsonify, Response
from flask.ext.babel import gettext

from oec import app, db, babel
from oec.utils import make_query
from oec.db_attr.models import Country, Sitc, Hs
from oec.explore.models import Build, App, Short
from sqlalchemy.sql.expression import func
from sqlalchemy import not_

mod = Blueprint('explore', __name__, url_prefix='/explore')

@mod.route('/')
def explore_redirect():
    '''fetch random country'''
    c = Country.query.filter(Country.id_2char != None) \
                        .filter(not_(Country.id.in_(["ocglp", "xxwld", "asymd", "eumco", "saguf", "euksv", "nabes", "astwn", "nacuw", "navir", "eusjm"]))) \
                        .order_by(func.random()).limit(1).first()
    
    return redirect(url_for('.explore', app_name="tree_map", \
                classification="hs", trade_flow="export", origin=c.id_3char, \
                dest="all", product="show", year="2011"))

def sanitize(app_name, classification, trade_flow, origin, dest, product, year):
    msg = None
    if classification == "hs":
        if origin in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=origin).first()
            origin = "zaf"
            msg = "{0} reports trade with South Africa in the HS classification".format(c.get_name())
        if dest in ["nam", "lso", "bwa", "swz"]:
            c = Country.query.filter_by(id_3char=dest).first()
            dest = "zaf"
            msg = "{0} reports trade with South Africa in the HS classification".format(c.get_name())
    
    if msg:
        flash(msg)
        return redirect(url_for('.explore', app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin=origin, dest=dest, product=product, year=year))

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def explore(app_name, classification, trade_flow, origin, dest, \
                product, year="2011"):
    g.page_type = mod.name
    redirect_resp = sanitize(app_name, classification, trade_flow, origin, dest, product, year)
    if redirect_resp: return redirect_resp
    
    current_app = App.query.filter_by(type=app_name).first_or_404()
    build_filters = {"origin":origin,"dest":dest,"product":product}
    for bf_name, bf in build_filters.items():
        if bf != "show" and bf != "all":
            build_filters[bf_name] = "<" + bf_name + ">"
    
    # raise Exception(current_app, trade_flow, build_filters["origin"], build_filters["dest"], build_filters["product"])
    current_build = Build.query.filter_by(app=current_app, trade_flow=trade_flow, 
                        origin=build_filters["origin"], dest=build_filters["dest"], 
                        product=build_filters["product"]).first_or_404()
    current_build.set_options(origin=origin, dest=dest, product=product, 
                                classification=classification, year=year)
    # raise Exception(current_build.data_url())
    # raise Exception(current_build.top_stats(5)["entries"][0])
    
    '''Every possible build for accordion links'''
    all_builds = Build.query.all()
    for i, build in enumerate(all_builds):
        build.set_options(origin=origin, dest=dest, product=product, classification=classification, year=year)
    # raise Exception(all_builds[10].data_url())
    
    kwargs = {"trade_flow":trade_flow, "origin_id":origin, "dest_id":dest, "year":year}
    if classification == "sitc":
        kwargs["sitc_id"] = product
    else:
        kwargs["hs_id"] = product
        
    # raise Exception(make_query(current_build.get_tbl(), request.args, g.locale, **kwargs))
    # raise Exception(current_build.top_stats(20))
    
    if session.pop('new_lang', None) and g.locale != 'en':
        flash_txt = '''We've noticed you've changed the language, if you see 
        some translations that look odd and you think you could do better feel 
        free to help us out by <a target="_blank" href="{0}">adding your 
        suggestions here</a>.'''.format(current_build.googledoc_url())
        flash(flash_txt)
    
    return render_template("explore/index.html",
        current_build = current_build,
        all_builds = all_builds)

@mod.route('/<app_name>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('/<app_name>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def explore_legacy(app_name, trade_flow, origin, dest, product, year='2011'):
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

    return render_template("explore/embed.html", current_build = current_build)

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