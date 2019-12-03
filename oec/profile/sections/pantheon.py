from flask_babel import gettext as _
import requests
import json

def format_pantheon_link(pantheon_obj, name_accessor="name"):
    profile_type = "person" if name_accessor == "name" else "place"
    return u"<a target='_blank' href='https://pantheon.world/profile/{}/{}/'>{}</a>".format(profile_type, pantheon_obj["slug"], pantheon_obj[name_accessor])

def make_pantheon_section(pantheon_id, attr):
    country_name = attr.get_name()
    memorable_people_xhr = requests.get('https://api.pantheon.world/person?select=name,hpi,id,slug,gender,birthyear,deathyear,bplace_country(id,country,continent,slug),bplace_geonameid(id,place,country,slug,lat,lon)&birthyear=gte.-3501&birthyear=lte.2015&bplace_country=eq.{}&hpi=gte.4&order=hpi.desc.nullslast&limit=10'.format(country_name))
    memorable_people = json.loads(memorable_people_xhr.text)

    memorable_places_xhr = requests.get('https://api.pantheon.world/place?select=place,hpi,id,slug,num_born&country=eq.{}&order=hpi.desc.nullslast&limit=10'.format(country_name))
    memorable_places = json.loads(memorable_places_xhr.text)

    pantheon_fields_iframe = "https://pantheon.world/explore/viz/embed?viz=treemap&show=occupations&years=-3501,2015&place={}".format(pantheon_id)
    pantheon_fields_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s, as proxied by the production of globally famous historical characters.", of_country=attr.get_name(article="of"))]
    if(memorable_people):
        memorable_people_as_links = [format_pantheon_link(p) for p in memorable_people]
        memorable_people_as_links_str = u", ".join(memorable_people_as_links[:-2] + [u" and ".join(memorable_people_as_links[-2:])])
        pantheon_fields_subtitle.append(u"The most memorable people born within the present day boundries of {} include {}.".format(country_name, memorable_people_as_links_str))
        # raise Exception(u"The most memorable people born within the present day boundries of {} include {}.".format(country_name, memorable_people_as_links_str))
    pantheon_fields_subtitle.append(u"<a target='_blank' class='viz_link' href='https://pantheon.world/explore/viz?viz=treemap&show=occupations&years=-3501,2015&place={}'>{} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
    pantheon_cities_iframe = "https://pantheon.world/explore/viz/embed?viz=treemap&show=places&years=-3501,2015&place={}".format(pantheon_id)
    pantheon_cities_subtitle = [_(u"This treemap shows the cultural exports %(of_country)s by city, as proxied by the production of globally famous historical characters.", of_country=attr.get_name(article="of"))]
    if(memorable_places):
        memorable_places_as_links = [format_pantheon_link(p, "place") for p in memorable_places]
        memorable_places_as_links_str = u", ".join(memorable_places_as_links[:-2] + [u" and ".join(memorable_places_as_links[-2:])])
        pantheon_cities_subtitle.append(u"The most common birth places of memorable people born within the present day boundries of {} include {}.".format(country_name, memorable_places_as_links_str))
    pantheon_cities_subtitle.append(u"<a target='_blank' class='viz_link' href='https://pantheon.world/explore/viz?viz=treemap&show=places&years=-3501,2015&place={0}'>{1} <i class='fa fa-external-link'></i></a>".format(pantheon_id, _("Explore on Pantheon")))
    
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
