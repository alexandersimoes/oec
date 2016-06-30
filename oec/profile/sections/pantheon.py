from flask.ext.babel import gettext as _

def make_pantheon_section(pantheon_id, attr):
    pantheon_fields_iframe = "http://pantheon.media.mit.edu/treemap/country_exports/{}/all/-4000/2010/H15/pantheon/embed".format(pantheon_id)
    pantheon_fields_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s, as proxied by the production of globally famous historical characters", of_country=attr.get_name(article="of"))]
    pantheon_fields_subtitle.append("<a target='_blank' href='http://pantheon.media.mit.edu/treemap/country_exports/{}/all/-4000/2010/H15/pantheon/'>{} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
    pantheon_cities_iframe = "http://pantheon.media.mit.edu/treemap/country_by_city/{0}/{0}/-4000/2010/H15/pantheon/embed".format(pantheon_id)
    pantheon_cities_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s by city, as proxied by the production of globally famous historical characters.", of_country=attr.get_name(article="of"))]
    pantheon_cities_subtitle.append("<a target='_blank' href='http://pantheon.media.mit.edu/treemap/country_by_city/{0}/{0}/-4000/2010/H15/pantheon/'>{1} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
    pantheon_section = {
        "title": "<a target='_blank' href='http://pantheon.media.mit.edu'><img src='http://pantheon.media.mit.edu/pantheon_logo.png' />",
        "source": "pantheon",
        "builds": [
            {"title": _(u"Globally Famous People %(of_country)s", of_country=attr.get_name(article="of")),
            "iframe": pantheon_fields_iframe,
            "subtitle": pantheon_fields_subtitle
            },
            {"title": _(u"Globally Famous People %(of_country)s by City", of_country=attr.get_name(article="of")),
            "iframe": pantheon_cities_iframe,
            "subtitle": pantheon_cities_subtitle
            },
        ]
    }
    
    return pantheon_section
