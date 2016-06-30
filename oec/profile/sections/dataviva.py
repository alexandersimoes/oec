from flask.ext.babel import gettext as _
from oec.db_attr.models import Country

def make_dv_section(self):
    if isinstance(self.attr, Country):
        if self.attr.id == "xxwld":
            dv_munic_dest_iframe = "http://legacy.dataviva.info/apps/embed/tree_map/secex/all/all/all/bra/?size=import_val&controls=false"
            dv_munic_dest_subtitle = [_(u"This treemap shows the municipalities in Brazil that imported products internationally.")]
            dv_munic_dest_subtitle.append(_(u"DataViva is a visualization tool that provides official data on trade, industries, and education throughout Brazil. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
            dv_munic_dest_subtitle.append(u"<a target='_blank' href='http://dataviva.info/en/location/all'>{} <i class='fa fa-external-link'></i></a>".format(_(u"Explore on DataViva")))
            dv_section = {
                "title": u"<a href='http://dataviva.info/' target='_blank'><img src='/static/img/dataviva_logo.png' /></a>",
                "source": "dataviva",
                "builds": [
                    {"title": _(u"Imports of Brazil by Municipality"), "iframe": dv_munic_dest_iframe, "subtitle": dv_munic_dest_subtitle}
                ]
            }
        elif self.attr.id == "sabra":
            dv_geo_map = "http://legacy.dataviva.info/apps/embed/geo_map/secex/all/all/all/bra/?color=export_val&controls=false&year=2013"
            dv_wages = "http://legacy.dataviva.info/apps/embed/bar/rais/all/all/all/bra/?controls=false&year=2013"
            dv_geo_map_subtitle = [_(u"This map shows the exports of Brazil by state.")]
            dv_geo_map_subtitle.append(_(u"DataViva is a visualization tool that provides official data on trade, industries, and education throughout Brazil. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
            dv_geo_map_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/en/location/all'>{} <i class='fa fa-external-link'></i></a>".format(_(u"Explore on DataViva")))

            dv_wages_subtitle = [_(u"This bar chart shows the wage distribution for the working population in Brazil.")]
            dv_wages_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/en/location/all'>{} <i class='fa fa-external-link'></i></a>".format(_(u"Explore on DataViva")))
        
            dv_section = {
                "title": u"<a href='http://dataviva.info/' target='_blank'><img src='/static/img/dataviva_logo.png' /></a>",
                "source": "dataviva",
                "builds": [
                    {"title": _(u"State Exports"), "iframe": dv_geo_map, "subtitle": dv_geo_map_subtitle},
                    {"title": _(u"Wage Distribution"), "iframe": dv_wages, "subtitle": dv_wages_subtitle},
                ]
            }
        else:
            dv_country_id = "asrus" if self.attr.id == "eurus" else self.attr.id
            dv_munic_dest_iframe = "http://legacy.dataviva.info/apps/embed/tree_map/secex/all/all/{}/bra/?size=import_val&controls=false".format(dv_country_id)
            dv_munic_origin_iframe = "http://legacy.dataviva.info/apps/embed/tree_map/secex/all/all/{}/bra/?size=export_val&controls=false".format(dv_country_id)
            dv_munic_dest_subtitle = []
            dv_munic_dest_subtitle.append(_(u"This treemap shows the municipalities in Brazil that imported products from %(country)s.", country=self.attr.get_name(article=True)))
            dv_munic_dest_subtitle.append(_(u"DataViva is a visualization tool that provides official data on trade, industries, and education throughout Brazil. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
            dv_munic_dest_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/en/trade_partner/{}'>{} <i class='fa fa-external-link'></i></a>".format(dv_country_id, _(u"Explore on DataViva")))
        
            dv_munic_origin_subtitle = []
            dv_munic_origin_subtitle.append(_(u"This treemap shows the municipalities in Brazil that exported products to %(country)s.", country=self.attr.get_name(article=True)))
            dv_munic_origin_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/en/trade_partner/{}'>{} <i class='fa fa-external-link'></i></a>".format(dv_country_id, _(u"Explore on DataViva")))
        
            dv_section = {
                "title": u"<a href='http://dataviva.info/' target='_blank'><img src='/static/img/dataviva_logo.png' /></a>",
                "source": "dataviva",
                "builds": [
                    {"title": _(u"Brazilian Municipalities that import from %(country)s", country=self.attr.get_name(article=True)), "iframe": dv_munic_dest_iframe, "subtitle": dv_munic_dest_subtitle},
                    {"title": _(u"Brazilian Municipalities that export to %(country)s", country=self.attr.get_name(article=True)), "iframe": dv_munic_origin_iframe, "subtitle": dv_munic_origin_subtitle},
                ]
            }
    else:
        dv_hs = self.attr
        if len(dv_hs.id) > 6:
            dv_hs = self.attr_cls.query.get(self.attr.id[:6])
        dv_munic_exporters_iframe = "http://legacy.dataviva.info/apps/embed/tree_map/secex/all/{}/all/bra/?controls=false&size=export_val".format(dv_hs.id)
        dv_munic_importers_iframe = "http://legacy.dataviva.info/apps/embed/tree_map/secex/all/{}/all/bra/?controls=false&size=import_val".format(dv_hs.id)

        dv_munic_exporters_subtitle = []
        dv_munic_exporters_subtitle.append(_(u"This treemap shows the municipalities in Brazil that export %(product)s.", product=dv_hs.get_name()))
        dv_munic_exporters_subtitle.append(_(u"DataViva is a visualization tool that provides official data on trade, industries, and education throughout Brazil. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
        dv_munic_exporters_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/apps/builder/tree_map/secex/all/{}/all/bra/?controls=false&size=export_val'>{} <i class='fa fa-external-link'></i></a>".format(self.attr.id, _(u"Explore on DataViva")))
        
        dv_munic_importers_subtitle = []
        dv_munic_importers_subtitle.append(_(u"This treemap shows the municipalities in Brazil that import %(product)s.", product=dv_hs.get_name()))
        dv_munic_importers_subtitle.append(_(u"DataViva is a visualization tool that provides official data on trade, industries, and education throughout Brazil. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
        dv_munic_importers_subtitle.append(u"<a target='_blank' href='http://legacy.dataviva.info/apps/builder/tree_map/secex/all/{}/all/bra/?controls=false&size=import_val'>{} <i class='fa fa-external-link'></i></a>".format(self.attr.id, _(u"Explore on DataViva")))
        
        dv_section = {
            "title": u"<a href='http://dataviva.info/' target='_blank'><img src='/static/img/dataviva_logo.png' /></a>",
            "source": "dataviva",
            "builds": [
                {"title": u"{} exporters in Brazil".format(dv_hs.get_name()), "iframe": dv_munic_exporters_iframe, "subtitle": dv_munic_exporters_subtitle},
                {"title": u"{} importers in Brazil".format(dv_hs.get_name()), "iframe": dv_munic_importers_iframe, "subtitle": dv_munic_importers_subtitle},
            ]
        }
        
    
    return dv_section