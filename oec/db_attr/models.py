from flask import g
from oec import db
from oec.utils import AutoSerialize, exist_or_404

class Country(db.Model, AutoSerialize):

    __tablename__ = 'attr_country'
    
    id = db.Column(db.String(5), primary_key=True)
    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.String(20))
    color = db.Column(db.String(7))
    comtrade_name = db.Column(db.String(255))
    
    name = db.relationship("Country_name", backref="country", lazy="joined")
    
    # attr_yo_origin = db.relationship("db_attr.models.Yo", backref = 'origin', lazy = 'dynamic')
    attr_yo = db.relationship("db_attr.models.Yo", backref = 'country', lazy = 'dynamic')
    
    hs_yodp_origin = db.relationship("db_hs.models.Yodp", primaryjoin = ('db_hs.models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs_yodp_dest = db.relationship("db_hs.models.Yodp", primaryjoin = ('db_hs.models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs_yod_dest = db.relationship("db_hs.models.Yod", primaryjoin = ('db_hs.models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs_yod_origin = db.relationship("db_hs.models.Yod", primaryjoin = ('db_hs.models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs_yop_origin = db.relationship("db_hs.models.Yop", primaryjoin = ('db_hs.models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    
    sitc_yodp_origin = db.relationship("db_sitc.models.Yodp", primaryjoin = ('db_sitc.models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    sitc_yodp_dest = db.relationship("db_sitc.models.Yodp", primaryjoin = ('db_sitc.models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    sitc_yod_dest = db.relationship("db_sitc.models.Yod", primaryjoin = ('db_sitc.models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    sitc_yod_origin = db.relationship("db_sitc.models.Yod", primaryjoin = ('db_sitc.models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    sitc_yop_origin = db.relationship("db_sitc.models.Yop", primaryjoin = ('db_sitc.models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    
    def get_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        _name = filter(lambda x: x.lang == lang, self.name)
        if len(_name):
            return _name[0].name
        return ""
    
    def get_attr_yo(self, year=2011):
        yo = filter(lambda yo: yo.year == year, self.attr_yo)
        if len(yo): return yo[0]
        return None
    
    def get_abbrv(self, lang=None):
        return self.id_3char if self.id_3char else ""
    
    def get_icon(self):
        return "/static/img/icons/country/country_%s.png" % (self.id)

    def serialize(self):
        auto_serialized = super(Country, self).serialize()
        auto_serialized["name"] = self.get_name()
        try:
            auto_serialized["display_id"] = auto_serialized.pop("id_3char")
        except KeyError:
            auto_serialized["display_id"] = None
        return auto_serialized
    
    def __repr__(self):
        return '<Country %r>' % (self.id)

class Country_name(db.Model, AutoSerialize):

    __tablename__ = 'attr_country_name'
    
    country_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(1))
    plural = db.Column(db.Boolean())
    article = db.Column(db.Boolean())
    
    def __repr__(self):
        return '<Country Name %r:%r>' % (self.country_id, self.lang)

class Hs(db.Model, AutoSerialize):

    __tablename__ = 'attr_hs'
    
    id = db.Column(db.String(8), primary_key=True)
    hs = db.Column(db.String(6))
    color = db.Column(db.String(7))
    
    name = db.relationship("Hs_name", backref="hs", lazy="joined")
    
    yodp_product = db.relationship("db_hs.models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_hs.models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_hs.models.Yp", backref = 'product', lazy = 'dynamic')
    
    classification = "hs"
    
    def get_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        _name = filter(lambda x: x.lang == lang, self.name)
        if len(_name):
            return _name[0].name
        return ""
    
    def get_abbrv(self, lang=None):
        return self.hs if self.hs else ""
    
    def get_icon(self):
        return "/static/img/icons/hs/hs_%s.png" % (self.id[:2])
    
    def serialize(self):
        auto_serialized = super(Hs, self).serialize()
        auto_serialized["name"] = self.get_name()
        try:
            auto_serialized["display_id"] = auto_serialized.pop("hs")
        except KeyError:
            auto_serialized["display_id"] = None
        return auto_serialized
    
    def __repr__(self):
        return '<Hs %r>' % (self.hs)

class Hs_name(db.Model, AutoSerialize):

    __tablename__ = 'attr_hs_name'
    
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    desc = db.Column(db.Text())
    gender = db.Column(db.String(1))
    plural = db.Column(db.Boolean())
    article = db.Column(db.Boolean())
    
    def __repr__(self):
        return '<Hs Name %r:%r>' % (self.hs_id, self.lang)

class Sitc(db.Model, AutoSerialize):

    __tablename__ = 'attr_sitc'
    
    id = db.Column(db.String(8), primary_key=True)
    sitc = db.Column(db.String(6))
    color = db.Column(db.String(7))
    
    name = db.relationship("Sitc_name", backref="sitc", lazy="joined")
    
    yodp_product = db.relationship("db_sitc.models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_sitc.models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_sitc.models.Yp", backref = 'product', lazy = 'dynamic')
    
    classification = "sitc"
    
    def get_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        _name = filter(lambda x: x.lang == lang, self.name)
        if len(_name):
            return _name[0].name
        return ""
    
    def get_abbrv(self, lang=None):
        return self.sitc if self.sitc else ""
    
    def get_icon(self):
        return "/static/img/icons/sitc/sitc_%s.png" % (self.id[:2])

    def serialize(self):
        auto_serialized = super(Sitc, self).serialize()
        auto_serialized["name"] = self.get_name()
        try:
            auto_serialized["display_id"] = auto_serialized.pop("sitc")
        except KeyError:
            auto_serialized["display_id"] = None
        return auto_serialized

    def __repr__(self):
        return '<Sitc %r>' % (self.sitc)

class Sitc_name(db.Model, AutoSerialize):

    __tablename__ = 'attr_sitc_name'
    
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    desc = db.Column(db.Text())
    gender = db.Column(db.String(1))
    plural = db.Column(db.Boolean())
    article = db.Column(db.Boolean())
    
    def __repr__(self):
        return '<Sitc Name %r:%r>' % (self.sitc_id, self.lang)

class Yo(db.Model, AutoSerialize):
    
    __tablename__ = 'attr_yo'
    
    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    eci = db.Column(db.Float())
    eci_rank = db.Column(db.Integer)
    opp_value = db.Column(db.Float())
    population = db.Column(db.Integer)
    gdp = db.Column(db.Numeric(16,2))
    gdp_pc = db.Column(db.Numeric(16,2))
    leader = db.Column(db.String(100))
    magic = db.Column(db.Float())
    pc_constant = db.Column(db.Float())
    pc_current = db.Column(db.Float())
    notpc_constant = db.Column(db.Float())
    
    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.origin_id)