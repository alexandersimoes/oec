from flask.ext.babel import gettext as _

def make_us_section():
    us_geo = "http://datausa.io/profile/geo/united-states/economy/income_geo/?viz=True"
    us_geo_text = [_(u"This map shows the states in the United States colored by median income.")]
    us_geo_text.append(_(u"Data USA is the most comprehensive visualization of U.S. public data. If you would like more info or to create a similar site get in touch with us at %(oec_email)s.", oec_email="<a href='mailto:oec@media.mit.edu'>oec@media.mit.edu</a>"))
    us_geo_text.append(u"<a target='_blank' href='http://datausa.io/profile/geo/united-states/#income_geo'>{} <i class='fa fa-external-link'></i></a>".format(_(u"Explore on Data USA")))
    
    us_distro = "http://datausa.io/profile/geo/united-states/economy/income_distro/?viz=True"
    us_distro_text = [_(u"This bar chart shows the wage distribution in the United States.")]
    us_distro_text.append(u"<a target='_blank' href='http://datausa.io/profile/geo/united-states/#income_distro'>{} <i class='fa fa-external-link'></i></a>".format(_(u"Explore on Data USA")))
    
    us_section = {
        "title": u"<a href='http://datausa.io/' target='_blank'><img src='/static/img/profile/datausa.png' /></a>",
        "source": "datausa",
        "builds": [
            {"title": _(u"Income by Location"), "iframe": us_geo, "subtitle": us_geo_text},
            {"title": _(u"Income by Location"), "iframe": us_distro, "subtitle": us_distro_text}
        ]
    }
    return us_section
