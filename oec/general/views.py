from operator import itemgetter
from datetime import datetime
from textblob import TextBlob
from fuzzywuzzy import process
from flask import Blueprint, render_template, g, request, current_app, \
                    session, redirect, url_for, flash, abort, jsonify
from flask.ext.babel import gettext

from oec.db_attr.models import Country, Country_name, Sitc, Sitc_name, Hs, Hs_name
from oec.explore.models import App, Build

import time, urllib2, json, itertools

mod = Blueprint('general', __name__, url_prefix='/')

from oec import app, db, babel

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    g.color = "#af1f24"
    g.page_type = mod.name
    g.supported_langs = current_app.config.get('LANGUAGES')
    
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
    
    # Set the locale to either 'pt' or 'en' on the global object
    if request.endpoint != 'static':
        # g.locale = "hi"
        # raise Exception(g.locale)
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
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    return "404"
    # g.page_type = "error404"
    # return render_template('general/404.html', error = e), 404

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
            return name_tbl.query \
                        .filter_by(lang=lang) \
                        .filter(name_tbl.name.like("%"+search_term+"%")).all()
        
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
        builds = []
        origins, dests, products = [[None]] * 3
        
        if len(countries):
            origins = countries[0]
        if len(countries) > 1:
            dests = countries[1]
        if len(hs_products) or len(sitc_products):
            products = sum([hs_products, sitc_products], [])
        
        combos = itertools.product([trade_flow], origins, dests, products)
        combos = [c for c in combos if len(set(filter(None, c))) == len(filter(None, c))]
        
        app = App.query.filter_by(type="tree_map").first()
        for combo in combos:
            trade_flow, origin, dest, product = combo
            classification = product.classification if product else "hs"
            # raise Exception(trade_flow, origin, dest, product, product.classification)
            
            all_builds = Build.query.filter_by(app=app)
            if trade_flow:
                all_builds = all_builds.filter_by(trade_flow=trade_flow)
            
            for i, build in enumerate(all_builds.all()):
                build.set_options(origin=origin, dest=dest, product=product, classification=classification)
                builds.append({"name": build.get_question(), "value": build.url()})
        
        return builds
    
    def results(self):
        lang = getattr(g, "locale", "en")
        excluded_tags = ['TO', 'DT']
        cleaned_words = [tag[0] for tag in self.text.tags if tag[1] not in excluded_tags]
        
        countries = self.get_attrs(cleaned_words, Country_name, "country", lang)
        sitc_products = sum(self.get_attrs(cleaned_words, Sitc_name, "sitc", lang), [])
        hs_products = sum(self.get_attrs(cleaned_words, Hs_name, "hs", lang), [])
        trade_flow = self.get_trade_flow(self.text)
        
        if len(countries) + len(sitc_products) + len(hs_products) == 0:
            return []
        
        builds = self.get_builds(countries, sitc_products, hs_products, trade_flow)
        builds_text = [b["name"] for b in builds]
        
        ordering = [result[0] for result in process.extract(self.text, builds_text, limit=20)]
        # raise Exception(ordering)
        
        raise Exception(map(itemgetter('text'), builds_text).index(ordering[0]))

###############################
# General views 
# ---------------------------
@mod.route('/')
def home():
    # Search('where does yemen export cheese?').results()
    # raise Exception(Search('where does yemen export cars to?').results())
    
    g.page_type = "home"
    ip = request.remote_addr
    
    # fetch the url
    url = "http://api.hostip.info/get_json.php?ip="+ip
    json_response = json.loads(urllib2.urlopen(url).read())
    country_code = json_response["country_code"]
    
    c = Country.query.filter_by(id_2char=country_code).first()
    if c is None:
        c = Country.query.filter_by(id="nausa").first()
    
    return render_template("home.html", default_country=c)

@mod.route('search/')
def search():
    query = request.args.get('q', '')
    results = {"items": Search(query).results()}
    return jsonify(results)

###############################
# API views 
# ---------------------------
@mod.route('book/')
def book():
    g.page_type = "book"
    return render_template("book/index.html")

###############################
# About views 
# ---------------------------
@mod.route('about/')
def about():
    g.page_type = "about"
    return render_template("about/index.html")

@mod.route('about/data/')
def about_data_redirect():
    return redirect(url_for('.about_data', data_type="sitc"))

@mod.route('about/data/<data_type>/')
def about_data(data_type):
    lang = request.args.get('lang', g.locale)
    
    if data_type == "sitc":
        items = Sitc.query.all()
        headers = ["Name", "SITC4 Code"]
        title = "SITC4 product names and codes"
    elif data_type == "hs":
        items = Hs.query.all()
        headers = ["Name", "HS4 Code"]
        title = "HS4 (harmonized system) product names and codes"
    elif data_type == "country":
        items = Country.query.all()
        headers = ["Name", "Alpha 3 Abbreviation"]
        title = "Country names and abbreviations"
    
    return render_template("about/data.html", items=items, headers=headers, title=title)

@mod.route('about/team/')
def about_team():
    return render_template("about/team.html")

@mod.route('about/permissions/')
def about_permissions():
    return render_template("about/permissions.html")

###############################
# API views 
# ---------------------------
@mod.route('api/')
def api():
    return redirect(url_for(".api_embed"))

@mod.route('api/embed/')
def api_embed():
    g.page_type = "api"
    return render_template("api/embed.html")

@mod.route('api/data/')
def api_data():
    g.page_type = "api"
    return render_template("api/data.html")