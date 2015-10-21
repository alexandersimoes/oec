# -*- coding: utf-8 -*-
import json
from flask import Blueprint, g, render_template
from oec import app
from oec.general.views import get_locale

mod = Blueprint('resources', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","vi","zh"):lang>/resources')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route('/about/')
def about():
    g.page_sub_type = "about"

    current = [
        {
            "name": u"Alexander Simoes",
            "slug": u"alexander_simoes",
            "time": u"2010 – Present",
            "text": u"Alex is the lead developer on the Observatory project. He has been working in the Macro Connections group developing technologies to better inform policy and decision makers by equipping them with tools to make sense of large datasets.",
            "links": {
                "github-alt": "https://github.com/alexandersimoes",
                "twitter": "https://twitter.com/ximoes",
                "linkedin-square": "http://www.linkedin.com/pub/alex-simoes/42/71a/728"
            }
        },
        {
            "name": u"Dave Landry",
            "slug": u"dave_landry",
            "time": u"2012 – Present",
            "text": u"Dave designed the 2013 version of the website, along with being co-author of the underlying visualization engine <a href='http://www.d3plus.org' target='_blank'>D3plus</a>. He continues to support the site with improvements to the front-end in both the visualizations and the overall navigation.",
            "links": {
                "github-alt": "https://github.com/davelandry",
                "twitter": "https://twitter.com/davelandry",
                "linkedin-square": "http://www.linkedin.com/in/davelandry/"
            }
        },
        {
            "name": u"César Hidalgo",
            "slug": u"cesar_hidalgo",
            "time": u"2010 – Present",
            "text": u"César is the Asahi Broadcast Corporation Career Development Professor and an Associate Professor at the MIT Media Lab. His work focuses on improving the understanding of systems using and developing concepts of complexity, evolution and network science.",
            "links": {
                "twitter": "https://twitter.com/cesifoti",
                "linkedin-square": "http://www.linkedin.com/pub/cesar-a-hidalgo/5/30a/a61"
            }
        },
        {
            "name": u"Melissa Teng",
            "slug": u"melissa_teng",
            "time": u"2015 – Present",
            "text": u"Melissa led the 2015 redesign of the website, focusing on a humanist approach to data. She built on the site's visual identity and user experience, as well as supported some front-end development.",
            "links": {
                "github-alt": "https://github.com/melteng",
                "twitter": "https://twitter.com/melisteng",
                "linkedin-square": "http://www.linkedin.com/in/mqteng/"
            }
        }
    ]

    past = [
        {
            "name": u"Eric Franco",
            "slug": u"eric_franco",
            "time": u"2012 – 2013",
            "text": u"Eric was responsible for maintaining the site and incorporating new data as it became available.",
            "links": {
                "github-alt": "https://github.com/ericjohnf",
                "linkedin-square": "http://www.linkedin.com/in/ericjohnf"
            }
        },
        {
            "name": u"Sarah Chung",
            "slug": u"sarah_chung",
            "time": u"2011 – 2012",
            "text": u"Sarah worked on developing algorithms for cleaning the raw SITC bilateral trade used on the site.",
            "links": {
                "linkedin-square": "http://www.linkedin.com/in/sarahchung7/"
            }
        },
        {
            "name": u"Crystal Noel",
            "slug": u"crystal_noel",
            "time": u"2011 – 2012",
            "text": u"Crystal helped improve some of the original visualizations and code-base.",
            "links": {
                "twitter": "https://twitter.com/crystalMIT13"
            }
        },
        {
            "name": u"Ali Almossawi",
            "slug": u"ali_almossawi",
            "time": u"2010 – 2011",
            "text": u"Ali was instrumental in the initial design, programming, and launch of The Observatory.",
            "links": {
                "github-alt": "https://github.com/almossawi",
                "twitter": "https://twitter.com/alialmossawi",
                "linkedin-square": "http://www.linkedin.com/in/almossawi"
            }
        }
    ]
    return render_template("resources/about.html", current=current, past=past)

@mod.route('/data/<data_type>/')
def data_classifications(data_type):
    g.page_type = "about"
    g.sub_page_type = "data"
    lang = request.args.get('lang', g.locale)
    download = request.args.get('download', None)

    if data_type == "sitc":
        items = Sitc.query.filter(Sitc.sitc != None).order_by(Sitc.sitc).all()
        headers = ["SITC", "Name"]
        title = "SITC4 product names and codes"
        id_col = "sitc"
    elif data_type == "hs":
        items = Hs.query.filter(Hs.hs != None).order_by(Hs.hs).all()
        headers = ["HS", "Name"]
        title = "HS4 (harmonized system) product names and codes"
        id_col = "hs"
    elif data_type == "country":
        items = Country.query.filter(Country.id_3char != None).order_by(Country.id_3char).all()
        headers = ["Abbrv", "Name"]
        title = "Country names and abbreviations"
        id_col = "id_3char"

    if download:
        s = StringIO()
        writer = csv.writer(s)
        title = "{0}_classification_list".format(data_type)
        writer.writerow([unicode(h).encode("utf-8") for h in headers])
        for i in items:
            writer.writerow([getattr(i, id_col), unicode(i.get_name()).encode("utf-8")])
        content_disposition = "attachment;filename={0}.csv".format(title)
        return Response(s.getvalue(),
                            mimetype="text/csv;charset=UTF-8",
                            headers={"Content-Disposition": content_disposition})

    return render_template("resources/data_classifications.html", items=items, headers=headers,
                            title=title, data_type=data_type, id_col=id_col)

@mod.route('/translations/')
def translations():
    g.page_type = "about"
    g.sub_page_type = "translations"
    return render_template("resources/translations.html")

@mod.route("/data/")
def data():
    g.page_sub_type = "data"
    return render_template("resources/data.html")

@mod.route('/faqs/')
def faqs():
    g.page_sub_type = "faqs"
    return render_template("resources/faqs.html")

@mod.route('/permissions/')
def permissions():
    g.page_type = "permissions"
    return render_template("resources/permissions.html")

@mod.route('/economic_complexity/')
def eci():
    g.page_type = "eci"
    return render_template("resources/eci.html")