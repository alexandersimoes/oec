import json, string, random
from datetime import datetime
from flask import g, url_for
from oec import db
from oec.db_attr.models import Country, Hs92, Hs96, Hs02, Hs07, Sitc
from config import FACEBOOK_ID

''' All the viz types currently supported
'''
all_viz = [
    {"slug":"tree_map", "name":"Tree Map", "color":"#333"},
    {"slug":"stacked", "name":"Stacked", "color":"#333"},
    {"slug":"network", "name":"Network", "color":"#333"},
    {"slug":"rings", "name":"Rings", "color":"#333"},
    {"slug":"scatter", "name":"Scatter", "color":"#333"},
    {"slug":"geo_map", "name":"Geo Map", "color":"#333"},
    {"slug":"line", "name":"Line", "color":"#333"}
]

''' Title, question, short name and category specific per build type. See below:
    0. tmap/stacked showing products exported/imported by country
    1. tmap/stacked showing destinations that a country exports to/imports from
    2. tmap/stacked of countries that export/import a product
    3. tmap/stacked of products exported/imported from a destination
    4. tmap/stacked of destinations that a country exports a product to
    5. network of product space
    6. rings
    7. scatter of PCI by GDP
    8. line chart of trade balance
'''
build_metadata = { \
    0: {
        "export": {
            "title": u"Products exported by {origin}",
            "question": u"What does {origin} export?",
            "short_name": "Exports",
            "category": "Country",
        },
        "import": {
            "title": u"Products imported by {origin}",
            "question": u"What does {origin} import?",
            "short_name": "Imports",
            "category": "Country"
        }
    },
    1: {
        "export": {
            "title": u"Import origins of {origin}",
            "question": u"Where does {origin} export to?",
            "short_name": "Export Destinations",
            "category": "Country"
        },
        "import": {
            "title": u"Export destinations of {origin}",
            "question": u"Where does {origin} import from?",
            "short_name": "Import Origins",
            "category": "Country"
        }
    },
    2: {
        "export": {
            "title": u"Countries that export {prod}",
            "question": u"Which countries export {prod}?",
            "short_name": "Exporters",
            "category": "Product"
        },
        "import": {
            "title": u"Countries that import {prod}",
            "question": u"Which countries import {prod}?",
            "short_name": "Importers",
            "category": "Product"
        }
    },
    3: {
        "export": {
            "title": u"Products that {origin} exports to {dest}",
            "question": u"What does {origin} export to {dest}?",
            "short_name": "Exports to Destination",
            "category": "Bilateral"
        },
        "import": {
            "title": u"Products that {origin} imports from {dest}",
            "question": u"What does {origin} import from {dest}?",
            "short_name": "Imports from Origin",
            "category": "Bilateral"
        }
    },
    4: {
        "export": {
            "title": u"Export destinations of {prod} from {origin}",
            "question": u"Where does {origin} export {prod} to?",
            "short_name": "Exports by Product",
            "category": "Bilateral"
        },
        "import": {
            "title": u"Import origins of {prod} to {origin}",
            "question": u"Where does {origin} import {prod} from?",
            "short_name": "Imports by Product",
            "category": "Bilateral"
        }
    },
    5: {
        "export": {
            "title": u"Product Space of {origin}",
            "question": u"What are the export opportunities of {origin}?",
            "short_name": "Product Space",
            "category": "Country"
        },
        "gini": {
            "title": u"GINI Product Space of {origin}",
            "question": u"What is the Product Gini of the exports of {origin}?",
            "short_name": "GINI Product Space",
            "category": "Country"
        }
    },
    6: {
        "export": {
            "title": u"Connections of {prod} in {origin}",
            "question": u"What does {origin} export that is similar to {prod}?",
            "short_name": "Product Connections",
            "category": "Country"
        }
    },
    7: {
        "gdp": {
            "title": u"Complexity compared to GDP",
            "question": u"How does complexity compare to GDP?",
            "short_name": "vs GDP",
            "category": "Economic Complexity"
        },
        "gdp_pc_constant": {
            "title": u"Complexity compared to GDP per capita (constant 2005 US$)",
            "question": u"How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc (constant '05 US$)",
            "category": "Economic Complexity"
        },
        "gdp_pc_current": {
            "title": u"Complexity compared to GDP per capita (current US$)",
            "question": u"How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc (current US$)",
            "category": "Economic Complexity"
        },
        "gdp_pc_constant_ppp": {
            "title": u"Complexity compared to GDP per capita, PPP (constant 2011 international $)",
            "question": u"How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc PPP (constant '11)",
            "category": "Economic Complexity"
        },
        "gdp_pc_current_ppp": {
            "title": u"Complexity compared to GDP per capita, PPP (constant 2011 international $)",
            "question": u"How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc PPP (current)",
            "category": "Economic Complexity"
        }
    },
    8: {
        "show": {
            "title": u"Trade balance of {origin}",
            "question": u"What is the trade balance for {origin}?",
            "short_name": "Trade Balance",
            "category": "Country"
        }
    },
    9: {
        "export": {
            "title": u"Connections of {prod}",
            "question": u"What products are {prod} connected to?",
            "short_name": "Product Connections",
            "category": "Product"
        }
    },
    10: {
        "eci": {
            "title": u"Country Rankings",
            "question": u"Country Rankings",
            "short_name": "All Countries",
            "category": "ECI Rankings"
        }
    },
    11: {
        "eci": {
            "title": u"Country Ranking for {dest}",
            "question": u"Country Ranking for {dest}",
            "short_name": "Specific Country",
            "category": "ECI Rankings"
        }
    },
    12: {
        "show": {
            "title": u"Trade balance of {origin} to {dest}",
            "question": u"What is the trade balance for {origin} to {dest}?",
            "short_name": "Trade Balance",
            "category": "Bilateral"
        }
    }
}

class Build(object):

    ''' Defaults used for a build if required by that build and the user
        has not specified one
    '''
    defaults = {
        "hs92": "0101", "hs96": "0101", "hs02": "0101", "hs07": "0101",
        "sitc": "5722",
        "country": "pry"
    }

    def __init__(self, viz="tree_map", classification="hs92", trade_flow="export", origin=None, dest=None, prod=None, year=None):
        self.viz = filter(lambda v: v["slug"]==viz, all_viz)[0]
        self.classification = classification
        self.trade_flow = trade_flow
        self.origin = self.get_country(origin)
        self.dest = self.get_country(dest)
        self.prod = self.get_prod(prod, classification)
        self.year = year if type(year) == list else [year]
        self.year_str = self.year_to_str(self.year)
        self.id = self.get_build_id(self.viz, origin, dest, prod)

    def get_country(self, country_id):
        if isinstance(country_id, Country):
            return country_id
        if country_id == "show" or country_id == "all":
            return country_id
        else:
            c = Country.query.filter_by(id_3char=country_id).first()
            if not c:
                c = Country.query.filter_by(id_3char=self.defaults["country"]).first()
            return c

    def get_prod(self, prod_id, classification):
        if isinstance(prod_id, (Hs92, Hs96, Hs02, Hs07, Sitc)):
            return prod_id
        if prod_id == "show" or prod_id == "all":
            return prod_id
        else:
            Prod = globals()[classification.capitalize()]
            p = Prod.query.filter(getattr(Prod, classification)==prod_id).first()
            if not p:
                p = Prod.query.filter(getattr(Prod, classification)==self.defaults[classification]).first()
            return p

    def year_to_str(self, year):
        if len(year) == 1:
            return year[0]
        else:
            interval = year[1] - year[0]
            if interval == 1:
                return "{}.{}".format(year[0], year[-1])
            else:
                return "{}.{}.{}".format(year[0], year[-1], interval)

    def get_build_id(self, viz, origin, dest, prod):
        '''build showing products given an origin'''
        if self.trade_flow == "show":
            return 8 if dest == "all" else 12
        if self.trade_flow == "eci":
            return 10 if dest == "all" else 11
        if viz["slug"] == "network":
            return 5
        if origin == "show" and dest == "all" and prod == "all":
            return 7
        if dest == "all" and prod == "show":
            return 0
        if dest == "show" and prod == "all":
            return 1
        if origin == "show":
            return 2
        if prod == "show":
            return 3
        if dest == "show":
            return 4
        if origin == "all":
            return 9
        if dest == "all":
            return 6

    def url(self, year=None):
        return "{viz}/{classification}/{trade_flow}/{origin}/{dest}/{prod}/{year}/".format(
            viz = self.viz["slug"],
            classification = self.classification,
            trade_flow = self.trade_flow,
            origin = getattr(self.origin, "id_3char", self.origin),
            dest = getattr(self.dest, "id_3char", self.dest),
            prod = getattr(self.prod, self.classification, self.prod),
            year = year or self.year_str,
        )

    def facebook_url(self):
        link = u"http://atlas.media.mit.edu/{}/visualize/{}".format(g.locale, self.url())
        return u"http://www.facebook.com/dialog/feed?caption=The Observatory of Economic Complexity&" \
                "display=popup&app_id={}&name={}&link={}&" \
                "redirect_uri=http://atlas.media.mit.edu/close/&" \
                "picture=http://atlas.media.mit.edu/static/img/facebook.jpg" \
                .format(FACEBOOK_ID, self.title(), link)
    def twitter_url(self):
        link = u"http://atlas.media.mit.edu/{}/visualize/{}".format(g.locale, self.url())
        lang_txt = u"&lang={}".format(g.locale) if g.locale != "en" else ""
        return u"https://twitter.com/share?url={}{}&text={}&hashtags=oec" \
                .format(link, lang_txt, self.title())
    def google_url(self):
        link = u"http://atlas.media.mit.edu/{}/visualize/{}".format(g.locale, self.url())
        return u"https://plus.google.com/share?url={}&hl={}" \
                .format(link, g.locale)

    def title(self):
        try:
            title = build_metadata[self.id][self.trade_flow]["title"]
        except KeyError:
            return None

        origin, dest, prod = None, None, None
        if isinstance(self.origin, Country):
            origin=self.origin.get_name(article="the")
        if isinstance(self.dest, Country):
            dest=self.dest.get_name(article="the")
        if isinstance(self.prod, (Hs92, Hs96, Hs02, Hs07, Sitc)):
            prod=self.prod.get_name()

        title = title.format(origin=origin, dest=dest, prod=prod)
        if len(self.year) == 1:
            years = self.year[0]
        else:
            years = u"{}-{}".format(self.year[0], self.year[-1])
        return u"{} ({})".format(title, years)

    def question(self):
        try:
            question = build_metadata[self.id][self.trade_flow]["question"]
        except KeyError:
            return None

        origin, dest, prod = None, None, None
        if isinstance(self.origin, Country):
            origin=self.origin.get_name(article="the")
        if isinstance(self.dest, Country):
            dest=self.dest.get_name(article="the")
        if isinstance(self.prod, (Hs92, Hs96, Hs02, Hs07, Sitc)):
            prod=self.prod.get_name()

        question = question.format(origin=origin, dest=dest, prod=prod)
        if len(self.year) == 1:
            years = self.year[0]
        else:
            years = "{}-{}".format(self.year[0], self.year[-1])
        return u"{} ({})".format(question, years)

    def short_name(self):
        return build_metadata[self.id][self.trade_flow]["short_name"]

    def category(self):
        return build_metadata[self.id][self.trade_flow]["category"]

    '''Returns the data URL for the specific build.'''
    def data_url(self, year=None, output_depth=None):

        if self.viz["slug"] == "line" and self.trade_flow == "eci":
            return "/attr/eci/"

        if self.viz["slug"] == "stacked" or self.viz["slug"] == "network":
            output_depth = 6
        elif self.viz["slug"] == "rings":
            output_depth = len(self.prod.id)
        output_depth = output_depth or 8
        year = year or self.year_str
        if not year:
            year = available_years[self.classification][-1]
        origin, dest, prod = [self.origin, self.dest, self.prod]
        xtra_args = ""
        if self.classification == "sitc":
            output_depth = 6

        if self.viz["slug"] == "rings" or (isinstance(prod, (Sitc, Hs92, Hs96, Hs02, Hs07)) and dest == "all" and isinstance(origin, Country)):
            prod = "show"
            xtra_args = "?output_depth={}_id_len.{}".format(self.classification, output_depth)
        elif isinstance(prod, (Sitc, Hs92, Hs96, Hs02, Hs07)):
            xtra_args = "?output_depth={}_id_len.{}".format(self.classification, len(prod.id))
            prod = getattr(prod, self.classification)

        if isinstance(origin, Country):
            origin = origin.id_3char
            xtra_args = "?output_depth={}_id_len.{}".format(self.classification, output_depth)
        if isinstance(dest, Country):
            dest = dest.id_3char
        url = '/{}/{}/{}/{}/{}/{}/{}'.format(self.classification,
                self.trade_flow, year, origin, dest, prod, xtra_args)
        return url

    def attr_url(self):
        lang = getattr(g, "locale", "en")
        if self.origin == "show" or self.dest == "show" or self.trade_flow == "show":
            return url_for('attr.attrs', attr='country', lang=lang)
        return url_for('attr.attrs', attr=self.classification, lang=lang)

    def attr_type(self):
        if self.origin == "show" or self.trade_flow == "show":
            return "origin"
        if self.dest == "show":
            return "dest"
        return self.classification

    def serialize(self):
        return json.dumps({
            "attr_type": self.attr_type(),
            "attr_url": self.attr_url(),
            "classification": self.classification,
            "data_url": self.data_url(),
            "dest": self.dest.serialize() if hasattr(self.dest, "serialize") else self.dest,
            "id": self.id,
            "lang": getattr(g, "locale", "en"),
            "origin": self.origin.serialize() if hasattr(self.origin, "serialize") else self.origin,
            "prod": self.prod.serialize() if hasattr(self.prod, "serialize") else self.prod,
            "social": {"facebook":self.facebook_url(),"twitter":self.twitter_url(),"google":self.google_url()},
            "title": self.title(),
            "trade_flow": self.trade_flow,
            "url": self.url(),
            "viz": self.viz,
            "year": self.year,
            "year_str": self.year_str,
        })

    def __repr__(self):
        return "<Build: {}:{}:{}:{}:{}>".format(self.viz["slug"], self.trade_flow, self.origin, self.dest, self.prod)

def get_all_builds(classification, origin_id, dest_id, prod_id, year, defaults, viz=None):
    if origin_id:
        origin_id = defaults["origin"] if any(x in origin_id for x in ["show", "all"]) else origin_id
    if dest_id:
        dest_id = defaults["dest"] if any(x in dest_id for x in ["show", "all"]) else dest_id
    if prod_id:
        prod_id = defaults["prod"] if any(x in prod_id for x in ["show", "all"]) else prod_id

    build_types = [
        {"origin": origin_id, "dest": "all", "prod": "show"},
        {"origin": origin_id, "dest": "show", "prod": "all"},
        {"origin": "show", "dest": "all", "prod": prod_id},
        {"origin": origin_id, "dest": dest_id, "prod": "show"},
        {"origin": origin_id, "dest": "show", "prod": prod_id},
    ]
    build_types = filter(lambda x: None not in x.values(), build_types)

    wanted_viz = all_viz
    if viz:
        viz = viz if isinstance(viz, list) else [viz]
        wanted_viz = filter(lambda v: v["slug"] in viz, all_viz)

    all_builds = []
    for v in wanted_viz:

        if any(x in v["slug"] for x in ["tree_map", "stacked"]):
            '''tree_map/stacked has all permutations of builds'''

            for b in build_types:
                for tf in ["export", "import"]:
                    build = Build(
                        viz = v["slug"],
                        classification = classification,
                        trade_flow = tf,
                        origin = b["origin"],
                        dest = b["dest"],
                        prod = b["prod"],
                        year = year)
                    all_builds.append(build)

        elif v["slug"] == "network":
            '''network aka product space only has 1 build'''

            build = Build(
                viz = v["slug"],
                classification = classification,
                trade_flow = "export",
                origin = origin_id,
                dest = "all",
                prod = "show",
                year = year)
            all_builds.append(build)
            
            build = Build(
                viz = v["slug"],
                classification = "sitc",
                trade_flow = "gini",
                origin = origin_id,
                dest = "all",
                prod = "show",
                year = year)
            all_builds.append(build)

        elif v["slug"] == "rings":
            '''rings has 1 builds'''

            build = Build(
                viz = v["slug"],
                classification = classification,
                trade_flow = "export",
                origin = origin_id,
                dest = "all",
                prod = prod_id,
                year = year)
            all_builds.append(build)

        elif v["slug"] == "scatter":
            '''scatter has builds using GDP'''

            for gdp_type in ["gdp", "gdp_pc_constant", "gdp_pc_current", "gdp_pc_constant_ppp", "gdp_pc_current_ppp"]:
                build = Build(
                    viz = v["slug"],
                    classification = classification,
                    trade_flow = gdp_type,
                    origin = "show",
                    dest = "all",
                    prod = "all",
                    year = year)
                all_builds.append(build)

        elif v["slug"] == "geo_map":
            '''geo map has builds for exporters/importers of a product'''

            for tf in ["export", "import"]:
                build = Build(
                    viz = v["slug"],
                    classification = classification,
                    trade_flow = tf,
                    origin = "show",
                    dest = "all",
                    prod = prod_id,
                    year = year)
                all_builds.append(build)

        elif v["slug"] == "line":

            '''trade balance'''
            all_builds.append(Build(viz = v["slug"],
                classification = classification,
                trade_flow = "show",
                origin = origin_id,
                dest = "all",
                prod = "all",
                year = year))

            '''all tree_map/stacked permutations'''
            for b in build_types:
                for tf in ["export", "import"]:
                    build = Build(
                        viz = v["slug"],
                        classification = classification,
                        trade_flow = tf,
                        origin = b["origin"],
                        dest = b["dest"],
                        prod = b["prod"],
                        year = year)
                    all_builds.append(build)

            all_builds.append(Build(viz = v["slug"],
                classification = classification,
                trade_flow = "show",
                origin = origin_id,
                dest = dest_id,
                prod = "all",
                year = year))

            '''eci rankings'''
            all_builds.append(Build(viz = v["slug"],
                classification = classification,
                trade_flow = "eci",
                origin = "show",
                dest = "all",
                prod = "all",
                year = year))

            all_builds.append(Build(viz = v["slug"],
                classification = classification,
                trade_flow = "eci",
                origin = "show",
                dest = dest_id,
                prod = "all",
                year = year))


    return all_builds

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
