# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template
from oec import app

mod = Blueprint('about', __name__, url_prefix='/about/')

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route('/')
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
            "text": u"Dave lead the 2013 redesign of the website, along with being co-author of the underlying visualization engine <a href='http://www.d3plus.org' target='_blank'>D3plus</a>. He continues to support the site with improvements to the front-end in both the visualizations and the overall navigation.",
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

    return render_template("about/index.html", current=current, past=past)

@mod.route('resources/')
def resources():
    return redirect(url_for('.about'))

def data_redirect():
    return redirect(url_for('.data_sources'))

@mod.route('data/<data_type>/')
def data(data_type):
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

    return render_template("about/data.html", items=items, headers=headers,
                            title=title, data_type=data_type, id_col=id_col)

@mod.route('translations/')
def translations():
    g.page_type = "about"
    g.sub_page_type = "translations"
    return render_template("about/translations.html")

@mod.route('updates/')
def updates():
    g.page_type = "about"
    g.sub_page_type = "updates"
    releases = json.load(urllib2.urlopen("https://api.github.com/repos/alexandersimoes/oec/releases"))
    updates = []
    for r in releases:
        u = {
            "title": r["name"],
            "body": markdown(r["body"]),
            "date": {
                "human": parser.parse(r["published_at"]).strftime("%A, %b %d %Y"),
                "meta": r["published_at"]
            },
            "url": r["html_url"]
        }
        updates.append(u)
    return render_template("about/updates.html", updates=updates)

###############################
# Legacy views (redirects)
# ---------------------------
@mod.route('api/')
@mod.route('api/embed/')
@mod.route('api/data/')
def api():
    return redirect(url_for("general.api"))

@mod.route('data/')
@mod.route('data/sources/')
@mod.route('data/download/')
def data_sources():
    return redirect(url_for('resources.data'))

@mod.route('permissions/')
def permissions():
    return redirect(url_for('general.permissions'))
