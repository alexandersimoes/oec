# -*- coding: utf-8 -*-
from flask import g, url_for
from flask.ext.babel import gettext as _
from datetime import datetime
from sqlalchemy import desc, not_, func
from oec import db, available_years, excluded_countries
from oec.utils import AutoSerialize, compile_query
from oec.db_attr.models import Country, Hs, Sitc
from oec.db_hs import models as hs_models
from oec.db_sitc import models as sitc_models

import ast, re, string, random

class App(db.Model, AutoSerialize):

    __tablename__ = 'explore_app'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(20))
    d3plus = db.Column(db.String(20))
    color = db.Column(db.String(7))

    def get_name(self):
        # lang = getattr(g, "locale", "en")
        # return getattr(self,"name_"+lang)
        return self.name

    def __repr__(self):
        return '<App %r>' % (self.type)

class Build_name(db.Model, AutoSerialize):

    __tablename__ = 'explore_build_name'

    # build_id = db.Column(db.Integer, db.ForeignKey(Build.id), primary_key = True)
    name_id = db.Column(db.Integer, primary_key = True)
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    short_name = db.Column(db.String(30))
    question = db.Column(db.String(255))
    category = db.Column(db.String(30))

    def __repr__(self):
        return '<Build Name %r:%r>' % (self.name_id, self.lang)

class Build(db.Model, AutoSerialize):

    __tablename__ = 'explore_build'

    app_id = db.Column(db.Integer, db.ForeignKey(App.id), primary_key = True)
    name_id = db.Column(db.Integer, db.ForeignKey(Build_name.name_id), primary_key = True)
    trade_flow = db.Column(db.String(20))
    origin = db.Column(db.String(20))
    dest = db.Column(db.String(20))
    product = db.Column(db.String(20))

    defaults = {
        "hs": "0101",
        "sitc": "5722",
        "country": "pry"
    }

    app = db.relationship('App',
            backref=db.backref('Builds', lazy='dynamic'))
    # name = db.relationship("Build_name", backref="build", lazy="joined")

    def get_year(self):
        if not self.year:
            return "2011"
        elif "." in self.year:
            years = self.year.split(".")
            return "{0} - {1}".format(years[0], years[1])
        else:
            return self.year

    def get_short_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        build_name = Build_name.query.filter_by(name_id=self.name_id, lang=lang).first()
        if build_name:
            return build_name.short_name
        else:
            return ""

    def get_category(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        build_name = Build_name.query.filter_by(name_id=self.name_id, lang=lang).first()
        if build_name:
            return build_name.category
        else:
            return ""

    def l18n_name(self, name, replace_term, item, lang):
        item_w_article = item.get_name(lang, article=True)
        attr_name = item.get_attr_name(lang)
        name_as_words = name.split(" ")
        prev_word_index = name_as_words.index(replace_term)-1
        prev_word = name_as_words[prev_word_index]

        ''' French! '''
        if lang == "fr":
            if prev_word == "<de>":
                prev_word = "de"
                if attr_name.article:
                    if item_w_article.startswith("le"):
                        prev_word = "du"
                        item_w_article = item_w_article.replace("le ", "")
                    if item_w_article.startswith("les"):
                        prev_word = "des"
                        item_w_article = item_w_article.replace("les ", "")
            if prev_word == u"<à>":
                prev_word = u"à"
                if attr_name.article:
                    if item_w_article.startswith("le"):
                        prev_word = "au"
                        item_w_article = item_w_article.replace("le ", "")
                    if item_w_article.startswith("les"):
                        prev_word = "aux"
                        item_w_article = item_w_article.replace("les ", "")
        ''' Spanish! '''
        if lang == "es":
            if prev_word == "<de>":
                prev_word = "de"
                if attr_name.article:
                    if item_w_article.startswith("el"):
                        prev_word = "del"
                        item_w_article = item_w_article.replace("el ", "")
            if prev_word == "<a>":
                prev_word = "a"
                if attr_name.article:
                    if item_w_article.startswith("el"):
                        prev_word = "al"
                        item_w_article = item_w_article.replace("el ", "")

        ''' Italian! '''
        if lang == "it":
            if attr_name.article:
                if item_w_article.startswith("il "): ending = "l"
                if item_w_article.startswith("lo "): ending = "llo"
                if item_w_article.startswith("l'"): ending = "ll'"
                if item_w_article.startswith("i "): ending = "i"
                if item_w_article.startswith("gli "): ending = "gli"
                if item_w_article.startswith("la "): ending = "lla"
                if item_w_article.startswith("le "): ending = "lle"
                item_w_article = item_w_article.replace("il ", "").replace("lo ", "").replace("l'", "") \
                    .replace("i ", "").replace("gli ", "").replace("la ", "").replace("le ", "")
                if prev_word == "<da>":
                    prev_word = "da" + ending
                if prev_word == "<di>":
                    prev_word = "de" + ending
                if prev_word == "<in>":
                    prev_word = "ne" + ending
            else:
                prev_word = prev_word.replace("<", "").replace(">", "")


        name_as_words[prev_word_index] = prev_word
        # raise Exception(name_as_words)
        name = " ".join(name_as_words)
        # if replace_term == "<dest>":
        #     raise Exception(name.replace(replace_term, unicode(item_w_article)))
        return name.replace(replace_term, u"<strong>{0}</strong>".format(item_w_article))

    def get_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        build_name = Build_name.query.filter_by(name_id=self.name_id, lang=lang).first()
        if build_name:
            name = build_name.name
        else:
            return ""

        if "<origin>" in name:
            name = self.l18n_name(name, "<origin>", self.origin, lang)
            # name = name.replace("<origin>", self.origin.get_name(lang, article=True))
        if "<dest>" in name:
            name = self.l18n_name(name, "<dest>", self.dest, lang)
            # name = name.replace("<dest>", self.dest.get_name(lang, article=True))
        if "<product>" in name:
            name = name.replace("<product>", u"<strong>{0}</strong>".format(self.product.get_name(lang, article=True)))

        return name

    def get_question(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        build_q = Build_name.query.filter_by(name_id=self.name_id, lang=lang).first()
        if build_q:
            q = build_q.question
        else:
            return ""

        if "<origin>" in q:
            q = q.replace("<origin>", self.origin.get_name(lang))
        if "<dest>" in q:
            q = q.replace("<dest>", self.dest.get_name(lang))
        if "<product>" in q:
            q = q.replace("<product>", self.product.get_name(lang))

        return q

    def get_ui(self, ui_type):
        return self.ui.filter(UI.type == ui_type).first()

    def set_options(self, origin=None, dest=None, product=None, classification="hs", year=2010):
        if year:
            self.year = year

        if self.origin != "show" and self.origin != "all":
            if isinstance(origin, Country):
                self.origin = origin
            else:
                self.origin = Country.query.filter_by(id_3char=origin).first_or_404()

        if self.dest != "show" and self.dest != "all":
            if isinstance(dest, Country):
                self.dest = dest
            else:
                self.dest = Country.query.filter_by(id_3char=dest).first_or_404()

        if self.product != "show" and self.product != "all":
            tbl = Sitc if classification == "sitc" else Hs
            if isinstance(product, (Sitc, Hs)):
                self.product = product
            else:
                self.product = tbl.query.filter(getattr(tbl, classification)==product).first()

        if classification:
            self.classification = classification

    '''Returns the URL for the specific build.'''
    def url(self, year=None):
        year = year or self.year
        if not year:
            year = available_years[self.classification][-1]
        if "." in str(year) and self.app.type != "stacked":
            year = year.split(".")[1]
        if "." not in str(year) and self.app.type == "stacked":
            year = "{0}.{1}".format(available_years[self.classification][0], available_years[self.classification][-1])
        origin, dest, product = [self.origin, self.dest, self.product]
        if isinstance(origin, Country):
            origin = origin.id_3char
        if isinstance(dest, Country):
            dest = dest.id_3char
        if isinstance(product, Hs):
            product = product.hs
        if isinstance(product, Sitc):
            product = product.sitc
        url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(self.app.type,
                self.classification, self.trade_flow, origin, dest,
                product, year)
        return url

    '''Returns the data URL for the specific build.'''
    def data_url(self, year=None):
        year = year or self.year
        if not year:
            year = available_years[self.classification][-1]
        origin, dest, product = [self.origin, self.dest, self.product]

        if (isinstance(product, Hs) and dest == "all" and isinstance(origin, Country)) or \
            (isinstance(product, Sitc) and dest == "all" and isinstance(origin, Country)):
            product = "show"
        elif isinstance(product, Hs):
            product = product.hs
        elif isinstance(product, Sitc):
            product = product.sitc
        if isinstance(origin, Country):
            origin = origin.id_3char
        if isinstance(dest, Country):
            dest = dest.id_3char
        url = '/{0}/{1}/{2}/{3}/{4}/{5}/'.format(self.classification,
                self.trade_flow, year, origin, dest, product)
        return url

    def attr_type(self):
        if self.origin == "show":
            return "origin"
        if self.dest == "show":
            return "dest"
        if self.classification == "sitc":
            return "sitc"
        return "hs"

    def attr_url(self):
        if self.origin == "show" or self.dest == "show":
            return url_for('attr.attrs', attr='country')
        if self.classification == "sitc":
            return url_for('attr.attrs', attr='sitc')
        return url_for('attr.attrs', attr='hs')

    def get_tbl(self):
        if self.classification == "hs":
            models = hs_models
        else:
            models = sitc_models

        if isinstance(self.origin, Country) and isinstance(self.dest, Country):
            return getattr(models, "Yodp")
        if isinstance(self.origin, Country) and isinstance(self.product, (Sitc, Hs)):
            return getattr(models, "Yodp")
        if isinstance(self.origin, Country) and self.product == "show":
            return getattr(models, "Yop")
        if isinstance(self.origin, Country) and self.dest == "show":
            return getattr(models, "Yod")
        if isinstance(self.product, (Sitc, Hs)) and self.origin == "show":
            return getattr(models, "Yop")

    def top_stats(self, entities=5):

        tbl = self.get_tbl()
        query = tbl.query

        if self.trade_flow == "export":
            query = query.order_by(tbl.export_val.desc()).filter(tbl.export_val != None)
            sum_query = db.session.query(db.func.sum(tbl.export_val))
        elif self.trade_flow == "import":
            query = query.order_by(tbl.import_val.desc()).filter(tbl.import_val != None)
            sum_query = db.session.query(db.func.sum(tbl.import_val))
        elif self.trade_flow == "net_export":
            query = db.session \
                        .query(tbl, tbl.export_val - tbl.import_val) \
                        .filter((tbl.export_val - tbl.import_val) > 0) \
                        .order_by(desc(tbl.export_val - tbl.import_val))
            sum_query = db.session.query(db.func.sum(tbl.export_val - tbl.import_val)).filter((tbl.export_val - tbl.import_val) > 0)
        elif self.trade_flow == "net_import":
            query = db.session \
                        .query(tbl, tbl.import_val - tbl.export_val) \
                        .filter((tbl.import_val - tbl.export_val) > 0) \
                        .order_by(desc(tbl.import_val - tbl.export_val))
            sum_query = db.session.query(db.func.sum(tbl.import_val - tbl.export_val)).filter((tbl.import_val - tbl.export_val) > 0)

        year = self.year
        if "." in str(year):
            year = str(year).split(".")[1]

        sum_query = sum_query.filter_by(year=year)
        query = query.filter_by(year=year)

        if isinstance(self.origin, Country):
            query = query.filter_by(origin_id=self.origin.id)
            sum_query = sum_query.filter_by(origin_id=self.origin.id)
        if isinstance(self.dest, Country):
            query = query.filter_by(dest_id=self.dest.id)
            sum_query = sum_query.filter_by(dest_id=self.dest.id)
        if isinstance(self.product, Sitc) and self.app.type != "rings":
            query = query.filter_by(sitc_id=self.product.id)
            sum_query = sum_query.filter_by(sitc_id=self.product.id)
        if isinstance(self.product, Hs) and self.app.type != "rings":
            query = query.filter_by(hs_id=self.product.id)
            sum_query = sum_query.filter_by(hs_id=self.product.id)

        sum = sum_query.first()[0]

        show_attr = {self.origin:"origin", self.dest:"dest", self.product:"product"}

        if show_attr.get("show", "product") == "origin":
            attr_name = _("Origin Country")
            attr_id_name = _("ID")
        elif show_attr.get("show", "product") == "dest":
            attr_name = _("Destination Country")
            attr_id_name = _("ID")
        elif show_attr.get("show", "product") == "product":
            attr_name = _("Product Name")
            attr_id_name = "SITC" if self.classification == "sitc" else "HS"

        header = ["Rank", attr_id_name, attr_name, self.trade_flow.title()+" Value", "Share"]

        stats = []
        for s in query.limit(entities).all():
            if self.trade_flow == "export":
                val = s.export_val
                attr = getattr(s, show_attr.get("show", "product"))
            if self.trade_flow == "import":
                val = s.import_val
                attr = getattr(s, show_attr.get("show", "product"))
            if self.trade_flow == "net_export":
                attr = getattr(s[0], show_attr.get("show", "product"))
                val = s[1]
            if self.trade_flow == "net_import":
                attr = getattr(s[0], show_attr.get("show", "product"))
                val = s[1]
            stat = {
                "attr": attr,
                "value": val,
                "share": 0
            }
            if(sum):
                stat["share"] = (val / sum) * 100
            stats.append(stat)

        return {"total":sum, "entries":stats, "header":header}

    def get_ui(self):
        ui = []

        if isinstance(self.origin, Country):
            # country_list = Country.query \
            #                 .filter(not_(Country.id.in_(excluded_countries))) \
            #                 .filter(Country.id_3char != None)
            # country_list = [c.serialize() for c in country_list]
            # country_list = sorted(country_list, key=lambda k: k['name'])
            country = {
                "id": "origin",
                "name": _("Origin"),
                "current": self.origin.serialize(),
                "url": url_for('attr.attrs', attr='country')
                # "data": country_list
            }
            ui.append(country)

        if isinstance(self.dest, Country):
            # country_list = Country.query \
            #                 .filter(not_(Country.id.in_(excluded_countries))) \
            #                 .filter(Country.id_3char != None)
            # country_list = [c.serialize() for c in country_list]
            # country_list = sorted(country_list, key=lambda k: k['name'])
            country = {
                "id": "destination",
                "name": _("Destination"),
                "current": self.dest.serialize(),
                # "data": country_list,
                "url": url_for('attr.attrs', attr='country')
            }
            ui.append(country)

        if isinstance(self.product, (Sitc, Hs)):
            # if self.classification == "sitc":
            #     product_list = Sitc.query \
            #                     .filter(func.char_length(Sitc.id)==6).all()
            # else:
            #     product_list = Hs.query \
            #                     .filter(func.char_length(Hs.id)==6).all()
            # product_list = [p.serialize() for p in product_list]
            # product_list = sorted(product_list, key=lambda k: k['name'])
            product = {
                "id": "product",
                "name": _("Product"),
                "current": self.product.serialize(),
                # "data": product_list,
                "url": url_for('attr.attrs', attr=self.classification)
            }
            ui.append(product)

        trade_flow = {
            "id": "trade_flow",
            "name": _("Trade Flow"),
            "current": self.trade_flow,
            "data": [
                {"name":_("Export"), "display_id":"export"},
                {"name":_("Import"), "display_id":"import"}
                # {"name":_("Net Export"), "display_id":"net_export"},
                # {"name":_("Net Import"), "display_id":"net_import"}
            ]
        }
        classification = {
            "id": "classification",
            "name": _("Classification"),
            "current": self.classification,
            "data": ["HS", "SITC"]
        }
        ui.append(trade_flow)

        if "." in self.year:
            year_parts = [int(y) for y in self.year.split(".")]
            if len(year_parts) == 2:
                years = range(year_parts[0], year_parts[1]+1)
            else:
                years = range(year_parts[0], year_parts[1]+1, year_parts[2])
            start_year = {
                "id": "start_year",
                "name": _("Start Year"),
                "current": years[0],
                "data": available_years[self.classification][::-1]
            }
            end_year = {
                "id": "end_year",
                "name": _("End Year"),
                "current": years[-1],
                "data": available_years[self.classification][::-1]
            }
            ui = ui + [start_year, end_year]
        else:
            year = {
                "id": "year",
                "name": _("Year"),
                "current": int(self.year),
                "data": available_years[self.classification][::-1]
            }
            ui.append(year)

        ui.append(classification)

        return ui

    def __repr__(self):
        return '<Build %d:%s>' % (self.name_id, self.app.type)

class Short(db.Model):

    __tablename__ = 'explore_short'

    slug = db.Column(db.String(30), unique=True, primary_key=True)
    long_url = db.Column(db.String(255), unique=True)
    created = db.Column(db.DateTime, default=datetime.now)
    clicks = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime)

    @staticmethod
    def make_unique_slug(long_url):

        # Helper to generate random URL string
        # Thx EJF: https://github.com/ericjohnf/urlshort
        def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        # test if it already exists
        short = Short.query.filter_by(long_url = long_url).first()
        if short:
            return short.slug
        else:
            while True:
                new_slug = id_generator()
                if Short.query.filter_by(slug = new_slug).first() == None:
                    break
            return new_slug

    def __repr__(self):
        return "<ShortURL: '%s'>" % self.long_url
