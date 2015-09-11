from flask import g
from sqlalchemy import func
from oec import db, available_years
from oec.utils import AutoSerialize

class ProdAttr(db.Model, AutoSerialize):
    __abstract__ = True
    id = db.Column(db.String(8), primary_key=True)
    conversion = db.Column(db.String(6))
    color = db.Column(db.String(7))

    def next(self):
        c = self.__class__
        return self.query.filter(c.id > self.id).filter(func.char_length(c.id)==len(self.id)).order_by(c.id).first()

    def prev(self):
        c = self.__class__
        return self.query.filter(c.id < self.id).filter(func.char_length(c.id)==len(self.id)).order_by(c.id.desc()).first()

    def get_attr_name(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        attr_name = self.name.filter_by(lang=lang).first()
        if attr_name:
            return attr_name.name
        return u""

    def get_name(self, lang=None, article=None, verb=None):
        lang = lang or getattr(g, "locale", "en")
        name = self.name.filter_by(lang=lang).first()
        if name:
            if lang == "en" and name.article and article:
                return "The {}".format(name.name)
            if lang == "en" and verb:
                verb = "are" if name.plural else "is"
                return "{} {}".format(name.name, verb)
            return name.name
        return ""

    def get_keywords(self, lang=None):
        lang = lang or getattr(g, "locale", "en")
        name = self.name.filter_by(lang=lang).first()
        if name:
            return name.keywords
        return ""

    def get_author(self):
        if hasattr(self, "image_link"):
            obj = None
            if self.image_link:
                obj = self

            if obj == None and len(self.id) >= 8:
                parent = self.__class__.query.get(self.id[:6])
                if parent.image_link:
                    obj = parent

            if obj == None and len(self.id) >= 4:
                parent = self.__class__.query.get(self.id[:2])
                if parent.image_link:
                    obj = parent

            if obj:
                obj = {
                    "link": obj.image_link,
                    "name": obj.image_author
                }
            return obj
        else:
            return None

    def get_image(self):
        if hasattr(self, "image_link"):
            if self.image_link:
                return "/static/img/headers/hs/{}.jpg".format(self.id)

            if len(self.id) >= 8:
                parent = self.__class__.query.get(self.id[:6])
                if parent.image_link:
                    return "/static/img/headers/hs/{}.jpg".format(self.id[:6])

            if len(self.id) >= 4:
                parent = self.__class__.query.get(self.id[:2])
                if parent.image_link:
                    return "/static/img/headers/hs/{}.jpg".format(self.id[:2])
        else:
            return None

    def get_display_id(self):
        if len(self.id) == 2:
            return self.id
        else:
            return getattr(self, self.classification)

    def get_top(self, limit=10, year=None):
        from oec import db_data
        year = year or available_years[self.classification][-1]
        Yo = getattr(db_data, "{}_models".format(self.classification)).Yo
        return Yo.query.filter_by(year=year, top_export=self.id)\
                .order_by(Yo.export_val.desc()).limit(limit)

    def get_yp(self, year=None):
        year = year or available_years[self.classification][-1]
        yp = filter(lambda yp: yp.year == year, self.yp_product)
        if len(yp): return yp[0]
        return None

    def get_abbrv(self, lang=None):
        return getattr(self, self.classification) if getattr(self, self.classification) else ""

    def get_icon(self):
        stem = "hs" if "hs" in self.classification else "sitc"
        return "/static/img/icons/{0}/{0}_{1}.png".format(stem, self.id[:2])

    def get_profile_url(self):
        return "/{}/profile/{}/{}/".format(g.locale, self.classification, getattr(self, self.classification))

    def get_profile_link(self):
        url = self.get_profile_url()
        name = self.get_name()
        return u'<a href="{}">{}</a>'.format(url, name)

    def serialize(self, lang="en"):
        auto_serialized = super(ProdAttr, self).serialize()
        auto_serialized["icon"] = self.get_icon()
        auto_serialized["image"] = self.get_image()
        try:
            auto_serialized["display_id"] = auto_serialized.pop(self.classification)
        except KeyError:
            auto_serialized["display_id"] = None
        return auto_serialized

    def __repr__(self):
        return '<Hs %r>' % (self.id)

class ProdNameAttr(object):
    lang = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    desc = db.Column(db.Text())
    gender = db.Column(db.String(1))
    plural = db.Column(db.Boolean())
    article = db.Column(db.Boolean())

    def __repr__(self):
        return '<Prod %r>' % (self.name)
