# -*- coding: utf-8 -*-
import ast
from abc import ABCMeta
from sqlalchemy import desc, func
from flask.ext.babel import gettext, pgettext
from oec import db, db_data, available_years
from oec.utils import num_format
from oec.db_attr import models as attrs
from oec.explore.models import Build

class Profile(object):

    __metaclass__ = ABCMeta

    def __init__(self, classification, id):
        self.classification = classification
        self.models = getattr(db_data, "{}_models".format(self.classification))
        self.id = id
        self.year = available_years[self.classification][-1]

    def title(self):
        return self.attr.get_attr_name().name

    def palette(self):
        if hasattr(self.attr, "palette"):
            p = self.attr.palette
        else:
            p = None
        if p:
            return ast.literal_eval(p)
        else:
            return ["#b7802b"]


class Country(Profile):

    def __init__(self, classification, id):
        super(Country, self).__init__(classification, id)
        self.attr = attrs.Country.query.filter_by(id_3char = self.id).first()

    @staticmethod
    def stringify_items(items, val=None, attr=None):
        str_items = []
        for i in items:
            if attr:
                this_attr = getattr(i, attr)
            else:
                this_attr = i
            if val:
                str_item = u"<a href='{}'>{}</a> ({})".format(this_attr.get_profile_url(), this_attr.get_name(), num_format(getattr(i, val)))
            else:
                str_item = u"<a href='{}'>{}</a>".format(this_attr.get_profile_url(), this_attr.get_name())
            str_items.append(str_item)
        if len(items) > 1:
            str_items = u"{0} {1} {2}".format(", ".join(str_items[:-1]), gettext("and"), str_items[-1])
        else:
            str_items = str_items[0]
        return str_items


    def intro(self):
        all_paragraphs = []
        ''' Paragraph #1
        '''
        this_yo = self.models.Yo.query.filter_by(year = self.year, country = self.attr).first()
        all_yo = self.models.Yo.query.filter_by(year = self.year).order_by(desc("export_val")).all()
        econ_rank = num_format(all_yo.index(this_yo) + 1, "ordinal")
        export_val = this_yo.export_val
        import_val = this_yo.import_val
        trade_balance = u"positive" if export_val > import_val else u"negative"
        this_attr_yo = attrs.Yo.query.filter_by(year = self.year, country = self.attr).first()
        eci_rank = this_attr_yo.eci_rank
        if eci_rank:
            eci_rank = u"and {} most complex by ECI ranking".format(num_format(eci_rank, "ordinal"))
        else:
            eci_rank = u""
        gdp = this_attr_yo.gdp
        gdp_pc = this_attr_yo.gdp_pc_current
        formatted_vals = {"export_val":export_val, "import_val":import_val, "gdp":gdp, "gdp_pc":gdp_pc}
        formatted_vals = {k: num_format(v) for k, v in formatted_vals.items()}
        p1 = u"The economy of {c} is the {econ_rank} largest economy in the world " \
                u"{eci_rank}. In {y}, {c} exported " \
                u"USD {export_val} in products and imported USD {import_val}, " \
                u"resulting in a {trade_balance} trade balance. In {y} the GDP of {c} " \
                u"was {gdp} and its GDP per capita was {gdp_pc}." \
                .format(c=self.attr.get_name(), y=self.year, econ_rank=econ_rank,
                    eci_rank=eci_rank, trade_balance=trade_balance, **formatted_vals)
        all_paragraphs.append(p1)

        ''' Paragraph #2
        '''
        yop_exp = self.models.Yop.query.filter_by(year = self.year, origin = self.attr).order_by(desc("export_val")).limit(5).all()
        exports_list = self.stringify_items(yop_exp, "export_val", "product")
        yop_imp = self.models.Yop.query.filter_by(year = self.year, origin = self.attr).order_by(desc("import_val")).limit(5).all()
        imports_list = self.stringify_items(yop_imp, "import_val", "product")
        p2 = u"The top exports of {} are {}, using the 1992 " \
                u"revision of the HS (harmonized system) classification. " \
                u"Its top imports are {}." \
                .format(self.attr.get_name(), exports_list, imports_list)
        all_paragraphs.append(p2)

        ''' Paragraph #3
        '''
        yod_exp = self.models.Yod.query.filter_by(year = self.year, origin = self.attr).order_by(desc("export_val")).limit(5).all()
        dest_list = self.stringify_items(yod_exp, "export_val", "dest")
        yod_imp = self.models.Yod.query.filter_by(year = self.year, dest = self.attr).order_by(desc("export_val")).limit(5).all()
        origin_list = self.stringify_items(yod_imp, "export_val", "origin")
        p3 = u"The top export destinations of {} are {}. " \
                u"The top import origins are {}." \
                .format(self.attr.get_name(), dest_list, origin_list)
        all_paragraphs.append(p3)

        ''' Paragraph #4
        '''
        land_borders = self.attr.borders()
        maritime_borders = self.attr.borders(maritime=True)
        if maritime_borders or land_borders:
            if maritime_borders and not land_borders:
                p4 = u"{} is an island and borders {} by sea.".format(self.attr.get_name(), self.stringify_items(maritime_borders))
            if not maritime_borders and land_borders:
                p4 = u"{} borders {}.".format(self.attr.get_name(), self.stringify_items(land_borders))
            if maritime_borders and land_borders:
                p4 = u"{} borders {} by land and {} by sea.".format(self.attr.get_name(), self.stringify_items(land_borders), self.stringify_items(maritime_borders))
            all_paragraphs.append(p4)

        return all_paragraphs

    def sections(self):
        ''' Trade Section
        '''
        export_tmap = Build("tree_map", "hs92", "export", self.attr, "all", "show", self.year)
        import_tmap = Build("tree_map", "hs92", "import", self.attr, "all", "show", self.year)
        dests_tmap = Build("tree_map", "hs92", "export", self.attr, "show", "all", self.year)
        origins_tmap = Build("tree_map", "hs92", "import", self.attr, "show", "all", self.year)
        trade_section = {
            "title": u"{} Trade".format(self.attr.get_name()),
            "builds": [
                {"title": u"Exports", "build": export_tmap},
                {"title": u"Imports", "build": import_tmap},
                {"title": u"Destinations", "build": dests_tmap},
                {"title": u"Origins", "build": origins_tmap},
            ]
        }

        ''' Product Space Section
        '''
        num_exports_w_rca = db.session.query(func.count(self.models.Yop.hs92_id)) \
                    .filter_by(year = self.year, origin = self.attr) \
                    .filter(self.models.Yop.export_rca >= 1) \
                    .filter(func.char_length(self.models.Yop.hs92_id)==6) \
                    .scalar()
        this_attr_yo = attrs.Yo.query.filter_by(year = self.year, country = self.attr).first()
        eci = this_attr_yo.eci
        eci_rank = this_attr_yo.eci_rank
        if eci_rank:
            subtitle = u"The economy of {} has an Economic Complexity Index (ECI) " \
                "of {} making it the {} most complex country. " \
                .format(self.attr.get_name(), num_format(eci), num_format(eci_rank, "ordinal"))
        else:
            subtitle = ""
        subtitle += u"{} exports {} products with revealed comparative advantage " \
            u"(meaning that its share of global exports is larger than what " \
            u"would be expected from the size of its export economy " \
            u"and from the size of a product’s global market)." \
            .format(self.attr.get_name(), num_exports_w_rca)
        product_space = Build("network", "hs92", "export", self.attr, "show", "all", self.year)
        ps_section = {
            "title": u"Export Opportunity in {}".format(self.attr.get_name()),
            "subtitle": subtitle,
            "builds": [
                {"title": u"Network", "build": product_space, "subtitle": u"The product space is a network connecting products that are likely to be co-exported and can be used to predict the evolution of a country’s export structure."},
            ]
        }

        ''' DataViva
        '''
        dv_munic_dest_iframe = "http://dataviva.info/apps/embed/tree_map/secex/all/all/{}/bra/?size=import_val".format(self.attr.id)
        dv_munic_origin_iframe = "http://dataviva.info/apps/embed/tree_map/secex/all/all/{}/bra/?size=export_val".format(self.attr.id)
        dv_section = {
            "title": "DataViva",
            "builds": [
                {"title": u"Brazilian Municipalities that import from {}".format(self.attr.get_name()), "iframe": dv_munic_dest_iframe, "subtitle": u"This treemap shows the municipalities in Brazil that imported products from {}.".format(self.attr.get_name())},
                {"title": u"Brazilian Municipalities that export to {}".format(self.attr.get_name()), "iframe": dv_munic_origin_iframe, "subtitle": u"This treemap shows the municipalities in Brazil that exported products to {}.".format(self.attr.get_name())},
            ]
        }

        ''' Pantheon
        '''
        pantheon_iframe = "http://pantheon.media.mit.edu/treemap/country_exports/{}/all/-4000/2010/H15/pantheon".format(self.attr.id_2char.upper())
        pantheon_section = {
            "title": "Pantheon",
            "builds": [
                {"title": u"Cultural Production of {}".format(self.attr.get_name()), "iframe": pantheon_iframe, "subtitle": u"This treemap shows the cultural exports of {}, as proxied by the production of globally famous historical characters.".format(self.attr.get_name(), self.year)},
            ]
        }


        return [trade_section, ps_section, dv_section]

class Product(Profile):
    pass
