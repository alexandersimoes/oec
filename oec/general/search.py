import itertools
from textblob import TextBlob
from sqlalchemy import desc, func
from flask import g
from oec.db_attr.models import Country, Country_name, Sitc, Sitc_name, Hs92, Hs92_name, \
                                Hs96, Hs96_name, Hs02, Hs02_name, Hs07, Hs07_name
from oec import db, db_data, available_years
from oec.visualize import models

class Search():
    text = None

    def __init__(self, text="", mode=["explore", "country", "hs92"], filter=None):
        self.text = TextBlob(text)
        self.mode = mode if hasattr(mode, '__iter__') else [mode]
        self.filter = filter
        self.classification = "hs92"
        self.trade_flow = "export"
        self.year = available_years[self.classification][-1]

    @staticmethod
    def get_attrs(words, name_tbl, attr_tbl_backref, lang, len_greater_than=None):
        # raise Exception(words, name_tbl, attr_tbl_backref, lang)
        found = []
        current_position = 0

        def look_in_db(search_term):
            base_q = name_tbl.query.filter_by(lang=lang)
            if len_greater_than:
                base_q = base_q.filter(func.char_length(name_tbl.id) > len_greater_than)
            
            exact_match = base_q.filter_by(name=search_term).first()
            if exact_match:
                return [exact_match]
            
            starts_with_match = base_q.filter(name_tbl.name.startswith(search_term)).all()
            if len(starts_with_match):
                return starts_with_match
            if attr_tbl_backref == "sitc" or attr_tbl_backref == "hs":
                return base_q.filter(name_tbl.name.like("%"+search_term+"%")).all()
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
    def get_builds_old(countries, sitc_products, hs_products, trade_flow):
        exact = []
        close = []
        origins, dests, products = [[None]] * 3

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
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()

            elif looking_for == "origin":
                entity = getattr(oec, "db_"+classification).models.Yop.query \
                            .filter_by(product=have) \
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()

            elif looking_for == "product":
                entity = getattr(oec, "db_"+classification).models.Yop.query \
                            .filter_by(origin=have) \
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()
            
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
                # raise Exception(default_product)
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
    
    def get_builds(self):
        origins, dests, products = [[None]] * 3

        if len(self.countries):
            origins = self.countries[0]
        if len(self.countries) > 1:
            dests = self.countries[1]
        if len(self.hs) or len(self.sitc):
            products = sum([self.hs, self.sitc], [])

        combos = itertools.product([self.trade_flow], origins, dests, products)
        combos = [c for c in combos if len(set(filter(None, c))) == len(filter(None, c))]
        
        def get_default(looking_for, have, trade_flow, classification, year):
            if looking_for == "dest":
                entity = getattr(db_data, "{}_models".format(classification)).Yod.query \
                            .filter_by(origin=have) \
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()

            elif looking_for == "origin":
                entity = getattr(db_data, "{}_models".format(classification)).Yop.query \
                            .filter_by(product=have) \
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()

            elif looking_for == "product":
                entity = getattr(db_data, "{}_models".format(classification)).Yop.query \
                            .filter_by(origin=have) \
                            .filter_by(year=available_years[classification][-1]) \
                            .order_by(desc(trade_flow+"_val")).limit(1).first()
        
            if entity:
                return getattr(entity, looking_for)
        
        exact = []
        for combo in combos[:4]:
            trade_flow, origin, dest, product = combo
            
            origin = origin or get_default("origin", dest, "export", "hs92", self.year)
            dest = dest or get_default("dest", origin, "export", "hs92", self.year)
            product = product or get_default("product", origin, "export", "hs92", self.year)
            
            # raise Exception([origin, dest, product])
            
            # origin, dest, product = map(lambda c: c.get_display_id(), [origin, dest, product])
            # origin, dest, product = [c.get_display_id() if c else c for c in [origin, dest, product]]
            origin = origin.get_display_id() if origin else None
            dest = dest.get_display_id() if dest else "all"
            product = product.get_display_id() if product else "all"
            
            defaults = {"origin":"nausa", "dest":"aschn", "prod":"010101"}
            builds = models.get_all_builds("hs92", origin, dest, product, self.year, defaults, viz=["tree_map","rings","network","geo_map"])
            
            for b in builds:
                exact.append({"value": b.question(), "name": b.url()})
        
        return exact

    def results(self):
        lang = getattr(g, "locale", "en")
        results = {}
        for m in self.mode:
            if m == "explore":
                excluded_tags = ['TO', 'DT']
                cleaned_words = [tag[0] for tag in self.text.tags if tag[1] not in excluded_tags]

                self.sitc, self.hs, trade_flow = [[]]*3
                self.countries = self.get_attrs(cleaned_words, Country_name, "country", lang)
        
                flat_countries = [item.get_name() for sublist in self.countries for item in sublist]

                country_words = [c.split() for c in flat_countries]
                country_words = [item for sublist in country_words for item in sublist]
                if len(country_words) < len(cleaned_words):
                    self.sitc = sum(self.get_attrs(cleaned_words, Sitc_name, "sitc", lang, 2), [])
                    self.hs = sum(self.get_attrs(cleaned_words, Hs92_name, "hs", lang, 2), [])
                    self.trade_flow = self.get_trade_flow(self.text) or "export"

                if len(self.countries) + len(self.sitc) + len(self.hs) == 0:
                    return []

                builds = self.get_builds()
                results[m] = builds
            else:
                Attr = globals()[m.title()]
                Attr_name = globals()["{}_name".format(m.title())]
                if m == "country":
                    Data_model = getattr(db_data, "{}_models".format(self.classification)).Yo
                    data_join_col = Data_model.origin_id
                else:
                    Data_model = getattr(db_data, "{}_models".format(m)).Yp
                    data_join_col = getattr(Data_model, "{}_id".format(m))
                query = db.session.query(Attr, Attr_name, Data_model) \
                        .filter(Attr.id == Attr_name.id) \
                        .filter(Attr_name.lang == lang) \
                        .filter(data_join_col == Attr.id) \
                        .filter(Data_model.year == available_years["country"][-1])
                if self.filter:
                    query = query.filter(Attr_name.id.startswith(self.filter))
                if self.text:
                    query = query.filter(Attr_name.name.contains(self.text))
                query = query.order_by(Data_model.export_val.desc())
                results[m] = [r[0].serialize() for r in query.all()]
        # raise Exception(results)
        return results
