# -*- coding: utf-8 -*-
from flask import g
from sqlalchemy import desc
from oec import db, __latest_year__, available_years
from oec.utils import AutoSerialize
from oec.db_attr.models import Country, Hs, Sitc
from oec.db_hs import models as hs_models
from oec.db_sitc import models as sitc_models

import ast, re

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
        "hs": "010101",
        "sitc": "105722",
        "country": "sapry"
    }
    
    app = db.relationship('App',
            backref=db.backref('Builds', lazy='dynamic'))
    # name = db.relationship("Build_name", backref="build", lazy="joined")
    
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
    
    def get_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        build_name = Build_name.query.filter_by(name_id=self.name_id, lang=lang).first()
        if build_name:
            name = build_name.name
        else:
            return ""
        
        if "<origin>" in name:
            name = name.replace("<origin>", self.origin.get_name(lang))
        if "<dest>" in name:
            name = name.replace("<dest>", self.dest.get_name(lang))
        if "<product>" in name:
            name = name.replace("<product>", self.product.get_name(lang))
        
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
        
        if self.origin != "show" and self.origin != "all":
            if isinstance(origin, Country):
                self.origin = origin
            elif origin == "all" or origin == "show":
                self.origin = Country.query.filter_by(id=self.defaults["country"]).first()
            else:
                self.origin = Country.query.filter_by(id=origin).first()
                if not self.origin:
                    self.origin = Country.query.filter_by(id=self.defaults["country"]).first()
        
        if self.dest != "show" and self.dest != "all":
            if isinstance(dest, Country):
                self.dest = dest
            elif dest == "all" or dest == "show":
                self.dest = Country.query.filter_by(id=self.defaults["country"]).first()
            else:
                self.dest = Country.query.filter_by(id=dest).first()
                if not self.dest:
                    self.dest = Country.query.filter_by(id=self.defaults["country"]).first()
        
        if self.product != "show" and self.product != "all":
            tbl = Sitc if classification == "sitc" else Hs
            if isinstance(product, (Sitc, Hs)):
                self.product = product
            else:
                if product == "all" or product == "show":
                    prod_id = self.defaults["sitc"] if classification == "sitc" else self.defaults["hs"]
                else:
                    prod_id = product
                self.product = tbl.query.filter_by(id=prod_id).first()
                if not self.product:
                    self.product = tbl.query.filter_by(id=self.defaults["hs"]).first()
        
        if classification:
            self.classification = classification
        
        if year:
            self.year = year
        
    '''Returns the URL for the specific build.'''
    def url(self, year=None):
        if not year:
            year = __latest_year__[self.classification]
        origin, dest, product = [self.origin, self.dest, self.product]
        if isinstance(origin, Country):
            origin = origin.id
        if isinstance(dest, Country):
            dest = dest.id
        if isinstance(product, (Hs, Sitc)):
            product = product.id
        url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(self.app.type, 
                self.classification, self.trade_flow, origin, dest, 
                product, year)
        return url

    '''Returns the data URL for the specific build.'''
    def data_url(self, year=None):
        year = self.year or year
        if not year:
            year = __latest_year__[self.classification]
        origin, dest, product = [self.origin, self.dest, self.product]
        if isinstance(origin, Country):
            origin = origin.id
        if isinstance(dest, Country):
            dest = dest.id
        if isinstance(product, (Hs, Sitc)):
            product = product.id
        url = '/{0}/{1}/{2}/{3}/{4}/{5}/'.format(self.classification, 
                self.trade_flow, year, origin, dest, product)
        return url

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

        sum_query = sum_query.filter_by(year=self.year)
        query = query.filter_by(year=self.year)
        
        if isinstance(self.origin, Country):
            query = query.filter_by(origin_id=self.origin.id)
            sum_query = sum_query.filter_by(origin_id=self.origin.id)
        if isinstance(self.dest, Country):
            query = query.filter_by(dest_id=self.dest.id)
            sum_query = sum_query.filter_by(dest_id=self.dest.id)
        if isinstance(self.product, Sitc):
            query = query.filter_by(sitc_id=self.product.id)
            sum_query = sum_query.filter_by(sitc_id=self.product.id)
        if isinstance(self.product, Hs):
            query = query.filter_by(hs_id=self.product.id)
            sum_query = sum_query.filter_by(hs_id=self.product.id)
            
        # raise Exception(self.year, self.origin, self.dest)
        # raise Exception(query.all())
        sum = sum_query.first()[0]
        
        show_attr = {self.origin:"origin", self.dest:"dest", self.product:"product"}
        
        stats = []
        for s in query.limit(entities).all():
            if self.trade_flow == "export":
                val = s.export_val
                attr = getattr(s, show_attr["show"])
            if self.trade_flow == "import":
                val = s.import_val
                attr = getattr(s, show_attr["show"])
            if self.trade_flow == "net_export":
                attr = getattr(s[0], show_attr["show"])
                val = s[1]
            if self.trade_flow == "net_import":
                attr = getattr(s[0], show_attr["show"])
                val = s[1]
            stat = {
                "attr": attr,
                "value": val,
                "share": (val / sum) * 100
            }
            stats.append(stat)
        
        return {"total":sum, "entries":stats}
    
    def get_ui(self):
        trade_flow = {
            "name": "Trade Flow",
            "current": self.trade_flow,
            "data": ["Export", "Import", "Net Export", "Net Import"]
        }
        year = {
            "name": "Year",
            "current": int(self.year),
            "data": available_years[self.classification]
        }
        classification = {
            "name": "Classification",
            "current": self.classification,
            "data": ["HS", "SITC"]
        }
        ui = [trade_flow, year]
        
        if isinstance(self.origin, Country):
            country_list = Country.query.filter(Country.id_3char != None)
            country = {
                "name": "Origin",
                "current": self.origin,
                "data": country_list
            }
            ui.append(country)
        
        if isinstance(self.dest, Country):
            country_list = Country.query.filter(Country.id_3char != None)
            country = {
                "name": "Destination",
                "current": self.dest,
                "data": country_list
            }
            ui.append(country)
        
        if isinstance(self.product, (Sitc, Hs)):
            if self.classification == "sitc":
                product_list = Sitc.query.all()
            else:
                product_list = Hs.query.all()
            product = {
                "name": "Product",
                "current": self.product,
                "data": product_list
            }
            ui.append(product)
        
        ui.append(classification)
        
        return ui
    
    def __repr__(self):
        return '<Build %d:%s>' % (self.name_id, self.app.type)
