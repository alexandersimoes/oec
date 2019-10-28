from flask_babel import gettext as _

def make_pantheon_section(pantheon_id, attr):
    pantheon_fields_iframe = "https://pantheon.world/explore/viz/embed?viz=treemap&show=occupations&years=-3501,2015&place={}".format(pantheon_id)
    pantheon_fields_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s, as proxied by the production of globally famous historical characters.", of_country=attr.get_name(article="of"))]
    pantheon_fields_subtitle.append(u"<a target='_blank' href='https://pantheon.world/explore/viz?viz=treemap&show=occupations&years=-3501,2015&place={}'>{} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
    pantheon_cities_iframe = "https://pantheon.world/explore/viz/embed?viz=treemap&show=places&years=-3501,2015&place={}".format(pantheon_id)
    pantheon_cities_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s by city, as proxied by the production of globally famous historical characters.", of_country=attr.get_name(article="of"))]
    pantheon_cities_subtitle.append(u"<a target='_blank' href='https://pantheon.world/explore/viz?viz=treemap&show=places&years=-3501,2015&place={0}'>{1} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
    pantheon_section = {
        "title": "<a target='_blank' href='https://pantheon.world'><img src='https://pantheon.world/images/logos/logo_pantheon.svg' />",
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
