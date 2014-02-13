from operator import itemgetter
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from sqlalchemy import not_
from datetime import datetime
from textblob import TextBlob
from fuzzywuzzy import process
from markdown import markdown
from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, jsonify, \
                    get_flashed_messages, Response
from flask.ext.babel import gettext

import oec
from oec.db_attr.models import Country, Country_name, Sitc, Sitc_name, Hs, Hs_name
from oec.explore.models import App, Build, Short

import time, urllib2, json, itertools
from dateutil import parser

import csv
from cStringIO import StringIO

mod = Blueprint('general', __name__, url_prefix='/')

from oec import app, db, babel, excluded_countries, available_years

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    g.page_type = mod.name
    g.supported_langs = current_app.config.get('LANGUAGES')
    g.available_years = available_years
    
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
    
    lang = request.args.get('lang', None)
    if lang:
        g.locale = get_locale(lang)
    
    if request.endpoint != 'static':
        g.locale = get_locale()

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    
    if lang:
        if lang in supported_langs:
            new_lang = lang
        session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif 'locale' in session:
            new_lang = session['locale']
        else:
            session['locale'] = new_lang
    
    return new_lang

###############################
# Set language views 
# ---------------------------
@mod.route('set_lang/<lang>/')
def set_lang(lang):
    g.locale = get_locale(lang)
    if lang != "en":
        session['new_lang'] = True
        flash_txt = '''We've noticed you've changed the language, if you see 
        some translations that look odd and you think you could do better feel 
        free to help us out by <a target="_blank" href="/about/translations/#{0}">
        adding your suggestions here</a>.'''.format(lang)
        flash(flash_txt, 'new_lang')
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    g.page_type = "error"
    return render_template('general/error.html', error = e), 404

class Search():
    text = None
    
    def __init__(self, text=""):
        self.text = TextBlob(text)
    
    @staticmethod
    def get_attrs(words, name_tbl, attr_tbl_backref, lang):
        # raise Exception(words, name_tbl, attr_tbl_backref, lang)
        found = []
        current_position = 0
        
        def look_in_db(search_term):
            exact_match = name_tbl.query \
                            .filter_by(lang=lang) \
                            .filter_by(name=search_term).first()
            if exact_match:
                return [exact_match]
            starts_with_match = name_tbl.query \
                                    .filter_by(lang=lang) \
                                    .filter(name_tbl.name.startswith(search_term)).all()
            if len(starts_with_match):
                return starts_with_match
            if attr_tbl_backref == "sitc" or attr_tbl_backref == "hs":
                return name_tbl.query \
                            .filter_by(lang=lang) \
                            .filter(name_tbl.name.like("%"+search_term+"%")).all()
            else:
                return []
        
        while current_position < len(words):
            search_term = words[current_position]
            names = look_in_db(search_term)
            num_found = len(names)
            
            if num_found == 1:
                found.append([getattr(name, attr_tbl_backref) for name in names])
                current_position += 1
            elif num_found > 1:
                temp_names = names
                
                if current_position == len(words) - 1:
                    found.append([getattr(name, attr_tbl_backref) for name in names])
                    current_position += 1
                
                for new_position in range(current_position+1, len(words)):
                    
                    new_search_term = " ".join(words[current_position:new_position+1])
                    new_names = look_in_db(new_search_term)
                    
                    if len(new_names) == 1:
                        found.append([getattr(name, attr_tbl_backref) for name in new_names])
                        current_position = new_position
                        break
                    if len(new_names) == 0 or len(new_names) > len(temp_names):
                        found.append([getattr(name, attr_tbl_backref) for name in temp_names])
                        # raise Exception(found, current_position, new_position)
                        current_position = new_position
                        break
                    if len(new_names) <= len(names):
                        temp_names = new_names
                        current_position = new_position
                        if new_position == len(words) - 1:
                            current_position = new_position
                            found.append([getattr(name, attr_tbl_backref) for name in temp_names])
            else:
                current_position += 1
        
        return found
    
    @staticmethod
    def get_trade_flow(text):
        if "net export" in text:
            return "net_export"
        if "net import" in text:
            return "net_import"
        if "import" in text:
            return "import"
        if "export" in text:
            return "export"
        return None

    @staticmethod
    def get_builds(countries, sitc_products, hs_products, trade_flow):
        exact = []
        close = []
        origins, dests, products = [[None]] * 3
        app = App.query.filter_by(type="tree_map").first()
        
        if len(countries):
            origins = countries[0]
        if len(countries) > 1:
            dests = countries[1]
        if len(hs_products) or len(sitc_products):
            products = sum([hs_products, sitc_products], [])
        
        combos = itertools.product([trade_flow], origins, dests, products)
        combos = [c for c in combos if len(set(filter(None, c))) == len(filter(None, c))]
        
        def get_default(looking_for, have, trade_flow, classification):
            if looking_for == "dest":
                entity = oec.db_hs.models.Yod.query \
                            .filter_by(origin=have) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()
            
            elif looking_for == "origin":
                entity = getattr(oec, "db_"+classification).models.Yop.query \
                            .filter_by(product=have) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()
            
            elif looking_for == "product":
                entity = getattr(oec, "db_"+classification).models.Yop.query \
                            .filter_by(origin=have) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()
            # raise Exception(getattr(entity, looking_for))
            if entity:
                return getattr(entity, looking_for)
        
        for combo in combos[:4]:
            exact = []
            close = []
            trade_flow, origin, dest, product = combo
            classification = product.classification if product else "hs"
            
            all_builds = Build.query.filter_by(app=app)
            if trade_flow:
                all_builds = all_builds.filter_by(trade_flow=trade_flow)
            
            # first test for country + product builds
            cp_builds = all_builds.filter_by(origin="<origin>", product="<product>")
            # for b in cp_builds.all()[1]:
            b = cp_builds.all()[0]
            if origin and product:
                b.set_options(origin=origin, dest=None, product=product, classification=classification)
                exact.append({"value": b.get_question(), "name": b.url()})
            elif origin:
                default_product = get_default("product", origin, b.trade_flow, classification)
                if default_product:
                    b.set_options(origin=origin, dest=None, product=default_product, classification=classification)
                    close.append({"value": b.get_question(), "name": b.url()})
            elif product:
                default_origin = get_default("origin", product, b.trade_flow, classification)
                if default_origin:
                    b.set_options(origin=default_origin, dest=None, product=product, classification=classification)
                    close.append({"value": b.get_question(), "name": b.url()})
            
            # test for country + country builds
            cc_builds = all_builds.filter_by(origin="<origin>", dest="<dest>")
            for b in cc_builds.all():
                if origin and dest:
                    b.set_options(origin=origin, dest=dest, product=None, classification=classification)
                    exact.append({"value": b.get_question(), "name": b.url()})
                elif origin:
                    default_dest = get_default("dest", origin, b.trade_flow, classification)
                    if default_dest:
                        b.set_options(origin=origin, dest=default_dest, product=None, classification=classification)
                        close.append({"value": b.get_question(), "name": b.url()})
            
            # test for country builds
            c_builds = all_builds.filter_by(origin="<origin>").filter(Build.dest!="<dest>").filter(Build.product!="<product>")
            for b in c_builds.all():
                if origin:
                    b.set_options(origin=origin, dest=None, product=None, classification=classification)
                    exact.append({"value": b.get_question(), "name": b.url()})
            
            # test for product builds
            p_builds = all_builds.filter_by(product="<product>").filter(Build.dest!="<dest>").filter(Build.origin!="<origin>")
            for b in p_builds.all():
                if product:
                    b.set_options(origin=None, dest=None, product=product, classification=classification)
                    exact.append({"value": b.get_question(), "name": b.url()})
            
            exact += exact
            close += close
        
        builds = exact + close
        # raise Exception(builds)
        return builds
    
    def results(self):
        lang = getattr(g, "locale", "en")
        excluded_tags = ['TO', 'DT']
        cleaned_words = [tag[0] for tag in self.text.tags if tag[1] not in excluded_tags]
        
        sitc_products, hs_products, trade_flow = [[]]*3
        countries = self.get_attrs(cleaned_words, Country_name, "country", lang)
        if len(countries) < len(cleaned_words):
            sitc_products = sum(self.get_attrs(cleaned_words, Sitc_name, "sitc", lang), [])
            hs_products = sum(self.get_attrs(cleaned_words, Hs_name, "hs", lang), [])
            trade_flow = self.get_trade_flow(self.text)
        
        if len(countries) + len(sitc_products) + len(hs_products) == 0:
            return []
        
        builds = self.get_builds(countries, sitc_products, hs_products, trade_flow)
        
        return builds
        
        # 
        # builds = self.get_builds(countries, sitc_products, hs_products, trade_flow)
        # builds_text = [b["value"] for b in builds]
        # 
        # ordering = [result[0] for result in process.extract(self.text, builds_text, limit=20)]
        # ordered_builds = [builds[map(itemgetter('value'), builds).index(b)] for b in ordering]
        # return ordered_builds

###############################
# General views 
# ---------------------------
@mod.route('/')
def home():
    g.page_type = "home"
    '''get user's country from IP address
    ip = request.remote_addr
    
    # fetch the url
    url = "http://api.hostip.info/get_json.php?ip="+ip
    json_response = json.loads(urllib2.urlopen(url).read())
    country_code = json_response["country_code"]
    '''
    
    '''get ramdom country'''
    c = Country.query.filter(Country.id_2char != None) \
                        .filter(not_(Country.id.in_(excluded_countries))) \
                        .order_by(func.random()).limit(1).first()
    current_app = App.query.filter_by(type="tree_map").first_or_404()
    default_build = Build.query.filter_by(app=current_app, name_id=1).first_or_404()
    default_build.set_options(origin=c, dest="all", product="show", classification="hs")
    
    return render_template("home.html", default_build=default_build)

@mod.route('search/')
def search():
    query = request.args.get('q', '')
    results = {"items": Search(query).results()}
    return jsonify(results)

###############################
# API views 
# ---------------------------
@mod.route('atlas/')
def atlas():
    g.page_type = "atlas"
    return render_template("atlas/index.html")

###############################
# About views 
# ---------------------------
@mod.route('about/')
def about():
    return redirect(url_for('.about_team'))

@mod.route('about/team/')
def about_team():
    g.page_type = "about"
    g.sub_title = "team"
    return render_template("about/team.html")

@mod.route('about/data/')
def about_data_redirect():
    return redirect(url_for('.about_data_sources'))

@mod.route('about/data/sources/')
def about_data_sources():
    g.page_type = "about"
    g.sub_title = "data"
    return render_template("about/data_sources.html", data_type="sources")

@mod.route('about/data/<data_type>/')
def about_data(data_type):
    g.page_type = "about"
    g.sub_title = "data"
    lang = request.args.get('lang', g.locale)
    download = request.args.get('download', None)
    
    if data_type == "sitc":
        items = Sitc.query.filter(Sitc.sitc != None).order_by(Sitc.sitc).all()
        headers = ["SITC", "Name"]
        title = "SITC4 product names and codes"
        id_col = "sitc"
    elif data_type == "hs":
        items = Hs.query.filter(Hs.hs != None).order_by(Hs.hs).all()
        headers = ["HS", "Name"]
        title = "HS4 (harmonized system) product names and codes"
        id_col = "hs"
    elif data_type == "country":
        items = Country.query.filter(Country.id_3char != None).order_by(Country.id_3char).all()
        headers = ["Abbrv", "Name"]
        title = "Country names and abbreviations"
        id_col = "id_3char"
    
    if download:
        s = StringIO()
        writer = csv.writer(s)
        title = "{0}_classification_list".format(data_type)
        writer.writerow([unicode(h).encode("utf-8") for h in headers])
        for i in items:
            writer.writerow([getattr(i, id_col), unicode(i.get_name()).encode("utf-8")])
        content_disposition = "attachment;filename={0}.csv".format(title)
        return Response(s.getvalue(), 
                            mimetype="text/csv;charset=UTF-8", 
                            headers={"Content-Disposition": content_disposition})
    
    return render_template("about/data.html", items=items, headers=headers, 
                            title=title, data_type=data_type, id_col=id_col)

@mod.route('about/permissions/')
def about_permissions():
    g.page_type = "about"
    g.sub_title = "permissions"
    return render_template("about/permissions.html")

@mod.route('about/faqs/')
def about_faqs():
    g.page_type = "about"
    g.sub_title = "faqs"
    return render_template("about/faqs.html")

@mod.route('about/translations/')
def about_translations():
    g.page_type = "about"
    g.sub_title = "translations"
    return render_template("about/translations.html")

@mod.route('about/updates/')
def about_updates():
    g.page_type = "about"
    g.sub_title = "updates"
    releases = json.load(urllib2.urlopen("https://api.github.com/repos/alexandersimoes/oec/releases"))
    updates = []
    for r in releases:
        u = {
            "title": r["name"], 
            "body": markdown(r["body"]), 
            "date": {
                "human": parser.parse(r["published_at"]).strftime("%A, %b %d %Y"),
                "meta": r["published_at"]
            },
            "url": r["html_url"]
        }
        updates.append(u)
    return render_template("about/updates.html", updates=updates)

###############################
# API views 
# ---------------------------
@mod.route('about/api/')
def api():
    return redirect(url_for(".api_embed"))

@mod.route('about/api/embed/')
def api_embed():
    g.page_type = "about"
    g.sub_title = "api"
    return render_template("about/api_embed.html", data_type="embed")

@mod.route('about/api/data/')
def api_data():
    g.page_type = "about"
    g.sub_title = "api"
    return render_template("about/api_data.html", data_type="data")

###############################
# Legacy support views
# ---------------------------
@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/')
@mod.route('embed/<app_name>/<trade_flow>/<origin>/<dest>/<product>/<year>/')
def embed_legacy(app_name, trade_flow, origin, dest, product, year='2011'):
    c = 'sitc' if int(year) < 1995 else 'hs'
    if product != "show" and product != "all":
        prod = Hs.query.filter_by(hs=product).first()
        c = 'hs'
        if not prod:
            c = 'sitc'
            prod = Sitc.query.filter_by(sitc=product).first()
        product = prod.id
    return redirect(url_for('explore.embed', app_name=app_name, \
                classification=c, trade_flow=trade_flow, origin=origin, \
                dest=dest, product=product, year=year))

###############################
# Handle shortened URLs
# ---------------------------
@mod.route('<slug>/')
def redirect_short_url(slug):
    short = Short.query.filter_by(slug = slug).first_or_404()
    short.clicks += 1
    short.last_accessed = datetime.utcnow()
    db.session.add(short)
    db.session.commit()
    
    return redirect(short.long_url)