from flask.ext.babel import gettext as _

def make_africa_section(self, africa_country):
    country_slug = africa_country[2]
    africa_crops_prod_val = "https://dataafrica.io/profile/{}/CropsByProduction?text=false".format(country_slug)
    africa_crops_prod_val_txt = [_(u"This treemap shows the crops produced in %(country)s sized by their production value.", country=self.attr.get_name(article=True))]
    africa_crops_prod_val_txt.append(_(u"Data Africa is an open-source platform designed to provide information on health, agriculture, climate, and poverty across 13 focus countries in Africa. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
    africa_crops_prod_val_txt.append(u"<a target='_blank' href='https://dataafrica.io/profile/{}#CropsByProduction'>{} <i class='fa fa-external-link'></i></a>".format(country_slug, _(u"Explore on Data Africa")))

    africa_crops_harv_area = "https://dataafrica.io/profile/{}/CropsByHarvest?text=false".format(country_slug)
    africa_crops_harv_area_txt = [_(u"This treemap shows the crops produced in %(country)s sized by their harvested area in hectares.", country=self.attr.get_name(article=True))]
    africa_crops_harv_area_txt.append(_(u"Data Africa is an open-source platform designed to provide information on health, agriculture, climate, and poverty across 13 focus countries in Africa. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
    africa_crops_harv_area_txt.append(u"<a target='_blank' href='https://dataafrica.io/profile/{}#CropsByHarvest'>{} <i class='fa fa-external-link'></i></a>".format(country_slug, _(u"Explore on Data Africa")))

    africa_section = {
        "title": u"<a href='https://dataafrica.io/' target='_blank'><img src='/static/img/profile/data-africa-wordmark.png' /></a>",
        "source": "dataafrica",
        "builds": [
            {"title": _(u"Crops by Production Value"), "iframe": africa_crops_prod_val, "subtitle": africa_crops_prod_val_txt},
            {"title": _(u"Crops by Harvested Area"), "iframe": africa_crops_harv_area, "subtitle": africa_crops_harv_area_txt}
        ]
    }
    return africa_section
