from oec.db_attr.models import Country, Hs92, Hs96, Hs02, Hs07, Sitc

''' All the viz types currently supported
'''
all_viz = [
    {"slug":"tree_map", "name":"Tree Map", "color":"#333"},
    {"slug":"stacked", "name":"Stacked", "color":"#333"},
    {"slug":"network", "name":"Network", "color":"#333"},
    {"slug":"rings", "name":"Rings", "color":"#333"},
    {"slug":"scatter", "name":"Scatter", "color":"#333"},
    {"slug":"geo_map", "name":"Geo Map", "color":"#333"}
]
test = 2

''' Title, question, short name and category specific per build type. See below:
    0. tmap/stacked showing products exported/imported by country
    1. tmap/stacked showing destinations that a country exports to/imports from
    2. tmap/stacked of countries that export/import a product
    3. tmap/stacked of products exported/imported from a destination
    4. tmap/stacked of destinations that a country exports a product to
    5. network of product space
    6. rings
    7. scatter of PCI by GDP
'''
build_metadata = { \
    0: {
        "export": {
            "title": "Products exported by {origin}",
            "question": "What does {origin} export?",
            "short_name": "Exports",
            "category": "Country"
        },
        "import": {
            "title":"Products imported by {origin}",
            "question": "What does {origin} import?",
            "short_name": "Imports",
            "category": "Country"
        }
    },
    1: {
        "export": {
            "title": "Import origins of {origin}",
            "question": "Where does {origin} export to?",
            "short_name": "Export Destinations",
            "category": "Country"
        },
        "import": {
            "title": "Export destinations of {origin}",
            "question": "Where does {origin} import from?",
            "short_name": "Import Origins",
            "category": "Country"
        }
    },
    2: {
        "export": {
            "title": "Countries that export {prod}",
            "question": "Which countries export {prod}?",
            "short_name": "Exporters",
            "category": "Product"
        },
        "import": {
            "title": "Countries that import {prod}",
            "question": "Which countries import {prod}?",
            "short_name": "Importers",
            "category": "Product"
        }
    },
    3: {
        "export": {
            "title": "Products that {origin} imports from {dest}",
            "question": "What does {origin} export to {dest}?",
            "short_name": "Exports to Destination",
            "category": "Bilateral"
        },
        "import": {
            "title": "Products that {origin} exports to {dest}",
            "question": "What does {origin} import from {dest}?",
            "short_name": "Imports from Origin",
            "category": "Bilateral"
        }
    },
    4: {
        "export": {
            "title": "Export destinations of {prod} from {origin}",
            "question": "Where does {origin} export {prod} to?",
            "short_name": "Exports by Product",
            "category": "Bilateral"
        },
        "import": {
            "title": "Import origins of {prod} to {origin}",
            "question": "Where does {origin} import {prod} from?",
            "short_name": "Imports by Product",
            "category": "Bilateral"
        }
    },
    5: {
        "export": {
            "title": "Product Space of {origin}",
            "question": "What does {origin} export?",
            "short_name": "Product Space",
            "category": None
        }
    },
    6: {
        "export": {
            "title": "Connections of {product} in {origin}",
            "question": "Where does {origin} export {prod} to?",
            "short_name": "Product Connections",
            "category": None
        }
    },
    7: {
        "gdp": {
            "title": "Complexity compared to GDP",
            "question": "How does complexity compare to GDP?",
            "short_name": "vs GDP",
            "category": "Economic Complexity"
        },
        "gdp_pc_constant": {
            "title": "Complexity compared to GDP per capita (constant 2005 US$)",
            "question": "How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc (constant '05 US$)",
            "category": "Economic Complexity"
        },
        "gdp_pc_current": {
            "title": "Complexity compared to GDP per capita (current US$)",
            "question": "How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc (current US$)",
            "category": "Economic Complexity"
        },
        "gdp_pc_constant_ppp": {
            "title": "Complexity compared to GDP per capita, PPP (constant 2011 international $)",
            "question": "How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc PPP (constant '11)",
            "category": "Economic Complexity"
        },
        "gdp_pc_current_ppp": {
            "title": "Complexity compared to GDP per capita, PPP (constant 2011 international $)",
            "question": "How does complexity compare to GDP per capita?",
            "short_name": "vs GDPpc PPP (current)",
            "category": "Economic Complexity"
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
        if viz == "network":
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
        if dest == "all":
            return 6

    def url(self):
        return "{viz}/{classification}/{trade_flow}/{origin}/{dest}/{prod}/{year}/".format(
            viz = self.viz["slug"],
            classification = self.classification,
            trade_flow = self.trade_flow,
            origin = getattr(self.origin, "id_3char", self.origin),
            dest = getattr(self.dest, "id_3char", self.dest),
            prod = getattr(self.prod, self.classification, self.prod),
            year = self.year_str,
        )

    def title(self):
        title = build_metadata[self.id][self.trade_flow]["title"]

        origin, dest, prod = None, None, None
        if isinstance(self.origin, Country):
            origin=self.origin.get_name()
        if isinstance(self.dest, Country):
            dest=self.dest.get_name()
        if isinstance(self.prod, (Hs92, Hs96, Hs02, Hs07, Sitc)):
            prod=self.prod.get_name()

        return title.format(origin=origin, dest=dest, prod=prod)

    def question(self):
        question = build_metadata[self.id][self.trade_flow]["question"]

        origin, dest, prod = None, None, None
        if isinstance(self.origin, Country):
            origin=self.origin.get_name()
        if isinstance(self.dest, Country):
            dest=self.dest.get_name()
        if isinstance(self.prod, (Hs92, Hs96, Hs02, Hs07, Sitc)):
            prod=self.prod.get_name()

        return question.format(origin=origin, dest=dest, prod=prod)

    def short_name(self):
        return build_metadata[self.id][self.trade_flow]["short_name"]

    def category(self):
        return build_metadata[self.id][self.trade_flow]["category"]

    def __repr__(self):
        return "<Build: {}:{}:{}:{}:{}>".format(self.viz["slug"], self.trade_flow, self.origin, self.dest, self.prod)

def get_all_builds(classification, origin_id, dest_id, prod_id, year, defaults, viz=None):
    origin_id = defaults["origin"] if any(x in origin_id for x in ["show", "all"]) else origin_id
    dest_id = defaults["dest"] if any(x in dest_id for x in ["show", "all"]) else dest_id
    try:
        prod_id = defaults["prod"] if any(x in prod_id for x in ["show", "all"]) else prod_id
    except:
        raise Exception(classification, origin_id, dest_id, prod_id, year, defaults, viz)

    build_types = [
        {"origin": origin_id, "dest": "all", "prod": "show"},
        {"origin": origin_id, "dest": "show", "prod": "all"},
        {"origin": "show", "dest": "all", "prod": prod_id},
        {"origin": origin_id, "dest": dest_id, "prod": "show"},
        {"origin": origin_id, "dest": "show", "prod": prod_id},
    ]

    wanted_viz = all_viz
    if viz:
        wanted_viz = filter(lambda v: v["slug"]==viz, all_viz)

    all_builds = []
    for v in wanted_viz:

        if any(x in v["slug"] for x in ["tree_map", "stacked"]):
            '''tree_map/stacked has all permutations of builds'''

            for tf in ["export", "import"]:
                for b in build_types:
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

        elif v["slug"] == "rings":
            '''rings only has 1 build'''

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


    return all_builds
