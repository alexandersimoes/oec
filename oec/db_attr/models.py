import ast
from flask import g
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from oec import db, available_years
from oec.utils import AutoSerialize, exist_or_404
from oec.db_attr.abstract_models import ProdAttr, ProdNameAttr

class Country(db.Model, AutoSerialize):

    __tablename__ = 'attr_country'

    id = db.Column(db.String(5), primary_key=True)
    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.String(20))
    color = db.Column(db.String(7))
    comtrade_name = db.Column(db.String(255))
    borders_land = db.Column(db.String(255))
    borders_maritime = db.Column(db.String(255))
    image_author = db.Column(db.String(200))
    image_link = db.Column(db.String(200))
    palette = db.Column(db.String(200))

    name = db.relationship("Country_name", backref="country", lazy="dynamic")

    # attr_yo_origin = db.relationship("db_attr.models.Yo", backref = 'origin', lazy = 'dynamic')
    attr_yo = db.relationship("db_attr.models.Yo", backref = 'country', lazy = 'dynamic')

    hs92_yo = db.relationship("db_data.hs92_models.Yo", backref = 'country', lazy = 'dynamic')
    hs96_yo = db.relationship("db_data.hs96_models.Yo", backref = 'country', lazy = 'dynamic')
    hs02_yo = db.relationship("db_data.hs02_models.Yo", backref = 'country', lazy = 'dynamic')
    hs07_yo = db.relationship("db_data.hs07_models.Yo", backref = 'country', lazy = 'dynamic')
    # sitc_yo = db.relationship("db_data.sitc_models.Yo", backref = 'country', lazy = 'dynamic')

    hs92_yodp_origin = db.relationship("db_data.hs92_models.Yodp", primaryjoin = ('db_data.hs92_models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs92_yodp_dest = db.relationship("db_data.hs92_models.Yodp", primaryjoin = ('db_data.hs92_models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs92_yod_dest = db.relationship("db_data.hs92_models.Yod", primaryjoin = ('db_data.hs92_models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs92_yod_origin = db.relationship("db_data.hs92_models.Yod", primaryjoin = ('db_data.hs92_models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs92_yop_origin = db.relationship("db_data.hs92_models.Yop", primaryjoin = ('db_data.hs92_models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    hs96_yodp_origin = db.relationship("db_data.hs96_models.Yodp", primaryjoin = ('db_data.hs96_models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs96_yodp_dest = db.relationship("db_data.hs96_models.Yodp", primaryjoin = ('db_data.hs96_models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs96_yod_dest = db.relationship("db_data.hs96_models.Yod", primaryjoin = ('db_data.hs96_models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs96_yod_origin = db.relationship("db_data.hs96_models.Yod", primaryjoin = ('db_data.hs96_models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs96_yop_origin = db.relationship("db_data.hs96_models.Yop", primaryjoin = ('db_data.hs96_models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    hs02_yodp_origin = db.relationship("db_data.hs02_models.Yodp", primaryjoin = ('db_data.hs02_models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs02_yodp_dest = db.relationship("db_data.hs02_models.Yodp", primaryjoin = ('db_data.hs02_models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs02_yod_dest = db.relationship("db_data.hs02_models.Yod", primaryjoin = ('db_data.hs02_models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs02_yod_origin = db.relationship("db_data.hs02_models.Yod", primaryjoin = ('db_data.hs02_models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs02_yop_origin = db.relationship("db_data.hs02_models.Yop", primaryjoin = ('db_data.hs02_models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    hs07_yodp_origin = db.relationship("db_data.hs07_models.Yodp", primaryjoin = ('db_data.hs07_models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs07_yodp_dest = db.relationship("db_data.hs07_models.Yodp", primaryjoin = ('db_data.hs07_models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs07_yod_dest = db.relationship("db_data.hs07_models.Yod", primaryjoin = ('db_data.hs07_models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    hs07_yod_origin = db.relationship("db_data.hs07_models.Yod", primaryjoin = ('db_data.hs07_models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    hs07_yop_origin = db.relationship("db_data.hs07_models.Yop", primaryjoin = ('db_data.hs07_models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    # sitc_yodp_origin = db.relationship("db_data.sitc_models.Yodp", primaryjoin = ('db_data.sitc_models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    # sitc_yodp_dest = db.relationship("db_data.sitc_models.Yodp", primaryjoin = ('db_data.sitc_models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    # sitc_yod_dest = db.relationship("db_data.sitc_models.Yod", primaryjoin = ('db_data.sitc_models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    # sitc_yod_origin = db.relationship("db_data.sitc_models.Yod", primaryjoin = ('db_data.sitc_models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    # sitc_yop_origin = db.relationship("db_data.sitc_models.Yop", primaryjoin = ('db_data.sitc_models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    # sitc_yodp_origin = db.relationship("db_sitc.models.Yodp", primaryjoin = ('db_sitc.models.Yodp.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    # sitc_yodp_dest = db.relationship("db_sitc.models.Yodp", primaryjoin = ('db_sitc.models.Yodp.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    # sitc_yod_dest = db.relationship("db_sitc.models.Yod", primaryjoin = ('db_sitc.models.Yod.dest_id == Country.id'), backref = 'dest', lazy = 'dynamic')
    # sitc_yod_origin = db.relationship("db_sitc.models.Yod", primaryjoin = ('db_sitc.models.Yod.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')
    # sitc_yop_origin = db.relationship("db_sitc.models.Yop", primaryjoin = ('db_sitc.models.Yop.origin_id == Country.id'), backref = 'origin', lazy = 'dynamic')

    def next(self):
        c = self.__class__
        return self.query.filter(c.id > self.id).filter(func.char_length(c.id)==len(self.id)).order_by(c.id).first()

    def prev(self):
        c = self.__class__
        return self.query.filter(c.id < self.id).filter(func.char_length(c.id)==len(self.id)).order_by(c.id.desc()).first()

    def get_attr_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        return self.name.filter_by(lang=lang).first()

    def get_name(self, lang=None, article=None):
        lang = lang or getattr(g, "locale", "en")
        name = self.name.filter_by(lang=lang).first()
        if name:
            ''' English '''
            if lang == "en" and name.article and article:
                return "The {0}".format(name.name)

            ''' French '''
            if lang == "fr" and name.article and article:
                if name.plural:
                    return u"les {0}".format(name.name)
                elif any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y']):
                    return u"l'{0}".format(name.name)
                elif name.gender == "m":
                    return u"le {0}".format(name.name)
                elif name.gender == "f":
                    return u"la {0}".format(name.name)

            ''' Spanish '''
            if lang == "es" and name.article and article:
                if name.gender == "m":
                    if name.plural:
                        return u"los {0}".format(name.name)
                    return u"el {0}".format(name.name)
                elif name.gender == "f":
                    if name.plural:
                        return u"las {0}".format(name.name)
                    return u"la {0}".format(name.name)

            ''' Italian '''
            if lang == "it" and name.article and article:
                if name.gender == "m":
                    if name.plural:
                        if any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y']):
                            return u"gli {0}".format(name.name)
                        if (name.name[0].lower() == "s"
                                and any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y'])) \
                                or name.name[0].lower() == "z":
                            return u"gli {0}".format(name.name)
                        return u"i {0}".format(name.name)
                    else:
                        if (name.name[0].lower() == "s"
                                and any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y'])) \
                                or name.name[0].lower() == "z":
                            return u"lo {0}".format(name.name)
                        if any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y']):
                            return u"l'{0}".format(name.name)
                        return u"il {0}".format(name.name)

                elif name.gender == "f":
                    if name.plural:
                        if any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y']):
                            return u"le {0}".format(name.name)
                        return u"le {0}".format(name.name)
                    else:
                        if any(vowel == name.name[0].lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y']):
                            return u"l'{0}".format(name.name)
                        return u"la {0}".format(name.name)

            return name.name
        return ""

    def get_display_id(self):
        return self.id_3char

    def get_attr_yo(self, year=None):
        year = year or available_years["country"][-1]
        yo = filter(lambda yo: yo.year == year, self.attr_yo)
        if len(yo): return yo[0]
        return None

    def get_abbrv(self, lang=None):
        return self.id_3char if self.id_3char else ""

    def get_icon(self):
        return "/static/img/icons/country/country_%s.png" % (self.id)

    def get_image(self):
        if self.image_link:
            return "/static/img/headers/country/{}.jpg".format(self.id)
        else:
            return None

    def get_top(self, limit=10, year=None):
        from oec.db_data.hs92_models import Yp
        year = year or available_years["country"][-1]
        return Yp.query.filter_by(year=year, top_exporter=self.id)\
                .order_by(Yp.export_val.desc()).limit(limit).all()

    def get_profile_url(self):
        if self.id_3char:
            return "/{}/profile/country/{}/".format(g.locale, self.id_3char)
        else:
            return "/{}/profile/country/".format(g.locale)

    def serialize(self, lang="en"):
        auto_serialized = super(Country, self).serialize()
        # auto_serialized["name"] = self.get_name(lang)
        auto_serialized["icon"] = self.get_icon()
        try:
            auto_serialized["display_id"] = auto_serialized.pop("id_3char")
        except KeyError:
            auto_serialized["display_id"] = None
        return auto_serialized

    def borders(self, maritime=False):
        if maritime:
            if not self.borders_maritime: return None
            border_countries = ast.literal_eval(self.borders_maritime)
        else:
            if not self.borders_land: return None
            border_countries = ast.literal_eval(self.borders_land)
        border_countries = self.query.filter(self.__class__.id.in_(border_countries)).all()
        return border_countries

    def __repr__(self):
        return '<Country %s>' % (self.id)

class Country_name(db.Model, AutoSerialize):

    __tablename__ = 'attr_country_name'

    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(1))
    plural = db.Column(db.Boolean())
    article = db.Column(db.Boolean())

    def __repr__(self):
        return '<Country Name %s:%s>' % (self.origin_id, self.lang)

class Hs92(ProdAttr):
    __tablename__ = 'attr_hs92'

    hs92 = db.Column(db.String(6))

    name = db.relationship("Hs92_name", backref="hs", lazy="dynamic")
    yodp_product = db.relationship("db_data.hs92_models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_data.hs92_models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_data.hs92_models.Yp", backref = 'product', lazy = 'dynamic')
    classification = "hs92"

class Hs96(ProdAttr):
    __tablename__ = 'attr_hs96'

    hs96 = db.Column(db.String(6))

    name = db.relationship("Hs96_name", backref="hs", lazy="dynamic")
    yodp_product = db.relationship("db_data.hs96_models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_data.hs96_models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_data.hs96_models.Yp", backref = 'product', lazy = 'dynamic')
    classification = "hs96"

class Hs02(ProdAttr):
    __tablename__ = 'attr_hs02'

    hs02 = db.Column(db.String(6))

    name = db.relationship("Hs02_name", backref="hs", lazy="dynamic")
    yodp_product = db.relationship("db_data.hs02_models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_data.hs02_models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_data.hs02_models.Yp", backref = 'product', lazy = 'dynamic')
    classification = "hs02"

class Hs07(ProdAttr):
    __tablename__ = 'attr_hs07'

    hs07 = db.Column(db.String(6))

    name = db.relationship("Hs07_name", backref="hs", lazy="dynamic")
    yodp_product = db.relationship("db_data.hs07_models.Yodp", backref = 'product', lazy = 'dynamic')
    yop_product = db.relationship("db_data.hs07_models.Yop", backref = 'product', lazy = 'dynamic')
    yp_product = db.relationship("db_data.hs07_models.Yp", backref = 'product', lazy = 'dynamic')
    classification = "hs07"

class Hs92_name(db.Model, AutoSerialize, ProdNameAttr):
    __tablename__ = 'attr_hs92_name'
    hs92_id = db.Column(db.String(8), db.ForeignKey(Hs92.id), primary_key=True)
    
    @hybrid_property
    def id(self):
        return self.hs92_id

class Hs96_name(db.Model, AutoSerialize, ProdNameAttr):
    __tablename__ = 'attr_hs96_name'
    hs96_id = db.Column(db.String(8), db.ForeignKey(Hs96.id), primary_key=True)
    
    @hybrid_property
    def id(self):
        return self.hs96_id

class Hs02_name(db.Model, AutoSerialize, ProdNameAttr):
    __tablename__ = 'attr_hs02_name'
    hs02_id = db.Column(db.String(8), db.ForeignKey(Hs02.id), primary_key=True)
    
    @hybrid_property
    def id(self):
        return self.hs02_id

class Hs07_name(db.Model, AutoSerialize, ProdNameAttr):
    __tablename__ = 'attr_hs07_name'
    hs07_id = db.Column(db.String(8), db.ForeignKey(Hs07.id), primary_key=True)
    
    @hybrid_property
    def id(self):
        return self.hs07_id

class Sitc(ProdAttr):
    __tablename__ = 'attr_sitc'
    sitc = db.Column(db.String(6))

    name = db.relationship("Sitc_name", backref="sitc", lazy="dynamic")
    # yodp_product = db.relationship("db_data.sitc_models.Yodp", backref = 'product', lazy = 'dynamic')
    # yop_product = db.relationship("db_data.sitc_models.Yop", backref = 'product', lazy = 'dynamic')
    # yp_product = db.relationship("db_data.sitc_models.Yp", backref = 'product', lazy = 'dynamic')
    classification = "sitc"

class Sitc_name(db.Model, AutoSerialize, ProdNameAttr):
    __tablename__ = 'attr_sitc_name'
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    
    @hybrid_property
    def id(self):
        return self.sitc_id
    

# class Hs(db.Model, AutoSerialize):
#
#     __tablename__ = 'attr_hs'
#
#     id = db.Column(db.String(8), primary_key=True)
#     hs = db.Column(db.String(6))
#     conversion = db.Column(db.String(6))
#     color = db.Column(db.String(7))
#
#     name = db.relationship("Hs_name", backref="hs", lazy="dynamic")
#
#     yodp_product = db.relationship("db_hs.models.Yodp", backref = 'product', lazy = 'dynamic')
#     yop_product = db.relationship("db_hs.models.Yop", backref = 'product', lazy = 'dynamic')
#     yp_product = db.relationship("db_hs.models.Yp", backref = 'product', lazy = 'dynamic')
#
#     classification = "hs"
#
#     def get_name(self, lang=None, article=None):
#         lang = lang or getattr(g, "locale", "en")
#         name = self.name.filter_by(lang=lang).first()
#         if name:
#             if lang == "en" and name.article and article:
#                 return "The {0}".format(name.name)
#             return name.name
#         return ""
#
#     def get_keywords(self, lang=None):
#         lang = lang or getattr(g, "locale", "en")
#         name = self.name.filter_by(lang=lang).first()
#         if name:
#             return name.keywords
#         return ""
#
#     def get_display_id(self):
#         return self.hs
#
#     def get_top(self, limit=10, year=available_years["hs"][-1]):
#         from oec.db_hs.models import Yo
#         return Yo.query.filter_by(year=year, top_export=self.id)\
#                 .order_by(Yo.export_val.desc()).limit(limit).all()
#
#     def get_yp(self, year=available_years["hs"][-1]):
#         yp = filter(lambda yp: yp.year == year, self.yp_product)
#         if len(yp): return yp[0]
#         return None
#
#     def get_abbrv(self, lang=None):
#         return self.hs if self.hs else ""
#
#     def get_icon(self):
#         return "/static/img/icons/hs/hs_%s.png" % (self.id[:2])
#
#     def get_profile_url(self):
#         return "/{}/profile/hs/{}/".format(g.locale, self.hs)
#
#     def serialize(self, lang="en"):
#         auto_serialized = super(Hs, self).serialize()
#         # auto_serialized["name"] = self.get_name(lang)
#         # auto_serialized["keywords"] = self.get_keywords()
#         auto_serialized["icon"] = self.get_icon()
#         try:
#             auto_serialized["display_id"] = auto_serialized.pop("hs")
#         except KeyError:
#             auto_serialized["display_id"] = None
#         return auto_serialized
#
#     def __repr__(self):
#         return '<Hs %r>' % (self.hs)
#
# class Hs_name(db.Model, AutoSerialize):
#
#     __tablename__ = 'attr_hs_name'
#
#     hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
#     lang = db.Column(db.String(5), primary_key=True)
#     name = db.Column(db.String(255))
#     keywords = db.Column(db.String(255))
#     desc = db.Column(db.Text())
#     gender = db.Column(db.String(1))
#     plural = db.Column(db.Boolean())
#     article = db.Column(db.Boolean())
#
#     def __repr__(self):
#         return '<Hs Name %r:%r>' % (self.hs_id, self.lang)
#
# class Sitc(db.Model, AutoSerialize):
#
#     __tablename__ = 'attr_sitc'
#
#     id = db.Column(db.String(8), primary_key=True)
#     sitc = db.Column(db.String(6))
#     conversion = db.Column(db.String(6))
#     color = db.Column(db.String(7))
#
#     name = db.relationship("Sitc_name", backref="sitc", lazy="dynamic")
#
#     yodp_product = db.relationship("db_sitc.models.Yodp", backref = 'product', lazy = 'dynamic')
#     yop_product = db.relationship("db_sitc.models.Yop", backref = 'product', lazy = 'dynamic')
#     yp_product = db.relationship("db_sitc.models.Yp", backref = 'product', lazy = 'dynamic')
#
#     classification = "sitc"
#
#     def get_name(self, lang=None, article=None):
#         lang = lang or getattr(g, "locale", "en")
#         name = self.name.filter_by(lang=lang).first()
#         if name:
#             if lang == "en" and name.article and article:
#                 return "The {0}".format(name.name)
#             return name.name
#         return ""
#
#     def get_keywords(self, lang=None):
#         lang = lang or getattr(g, "locale", "en")
#         name = self.name.filter_by(lang=lang).first()
#         if name:
#             return name.keywords
#         return ""
#
#     def get_display_id(self):
#         return self.sitc
#
#     def get_abbrv(self, lang=None):
#         return self.sitc if self.sitc else ""
#
#     def get_icon(self):
#         return "/static/img/icons/sitc/sitc_%s.png" % (self.id[:2])
#
#     def get_profile_url(self):
#         return "/profile/sitc/"+self.sitc+"/"
#
#     def get_top(self, limit=10, year=available_years["sitc"][-1]):
#         from oec.db_sitc.models import Yp
#         return Yp.query.filter_by(year=year, top_exporter=self.id)\
#                 .order_by(Yp.export_val.desc()).limit(limit).all()
#
#     def get_yp(self, year=2010):
#         yp = filter(lambda yp: yp.year == year, self.yp_product)
#         if len(yp): return yp[0]
#         return None
#
#     def serialize(self, lang="en"):
#         auto_serialized = super(Sitc, self).serialize()
#         # auto_serialized["name"] = self.get_name(lang)
#         # auto_serialized["keywords"] = self.get_keywords()
#         auto_serialized["icon"] = self.get_icon()
#         try:
#             auto_serialized["display_id"] = auto_serialized.pop("sitc")
#         except KeyError:
#             auto_serialized["display_id"] = None
#         return auto_serialized
#
#     def __repr__(self):
#         return '<Sitc %r>' % (self.sitc)
#
# class Sitc_name(db.Model, AutoSerialize):
#
#     __tablename__ = 'attr_sitc_name'
#
#     sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
#     lang = db.Column(db.String(5), primary_key=True)
#     name = db.Column(db.String(255))
#     keywords = db.Column(db.String(255))
#     desc = db.Column(db.Text())
#     gender = db.Column(db.String(1))
#     plural = db.Column(db.Boolean())
#     article = db.Column(db.Boolean())
#
#     def __repr__(self):
#         return '<Sitc Name %r:%r>' % (self.sitc_id, self.lang)

class Yo(db.Model, AutoSerialize):

    __tablename__ = 'attr_yo'

    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    eci = db.Column(db.Float())
    eci_rank = db.Column(db.Integer)
    eci_rank_delta = db.Column(db.Integer)
    opp_value = db.Column(db.Float())
    population = db.Column(db.Integer)
    gdp = db.Column(db.Numeric(16,2))
    gdp_pc_constant = db.Column(db.Numeric(16,2))
    gdp_pc_current = db.Column(db.Numeric(16,2))
    gdp_pc_constant_ppp = db.Column(db.Numeric(16,2))
    gdp_pc_current_ppp = db.Column(db.Numeric(16,2))
    leader = db.Column(db.String(100))
    magic = db.Column(db.Float())
    pc_constant = db.Column(db.Float())
    pc_current = db.Column(db.Float())
    notpc_constant = db.Column(db.Float())

    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.origin_id)
