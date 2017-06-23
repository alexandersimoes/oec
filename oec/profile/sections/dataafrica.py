from flask.ext.babel import gettext as _

def make_africa_section(self, africa_country):
    country_slug = africa_country[2]
    africa_crops = "https://dataafrica.io/profile/{}/CropsByProduction".format(country_slug)
    africa_crops_text = [_(u"This treemap shows the crops in %(country)s by production value.", country=self.attr.get_name(article=True))]
    africa_crops_text.append(_(u"Data Africa is an open source agriculture, climate, poverty, and health visualization engine. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
    africa_crops_text.append(u"<a target='_blank' href='https://dataafrica.io/profile/{}#CropsByProduction'>{} <i class='fa fa-external-link'></i></a>".format(country_slug, _(u"Explore on Data Africa")))

    africa_section = {
        "title": u"<a href='https://dataafrica.io/' target='_blank'><img src='/static/img/profile/data-africa-wordmark.png' /></a>",
        "source": "dataafrica",
        "builds": [
            {"title": _(u"Crops By Production"), "iframe": africa_crops, "subtitle": africa_crops_text}
        ]
    }
    return africa_section
