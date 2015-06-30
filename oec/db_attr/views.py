from oec import db
from flask import Blueprint, request, jsonify, make_response, g, render_template
# from oec.db_attr.models import Country, Country_name, Hs, Hs_name, Sitc, Sitc_name
from oec.db_attr.models import *
from oec.decorators import crossdomain

mod = Blueprint('attr', __name__, url_prefix='/attr')

############################################################
# ----------------------------------------------------------
# All attribute views
#
############################################################

@mod.route('/<attr>/')
@mod.route('/<attr>/<lang>/')
@crossdomain(origin='*')
def attrs(attr="country", lang='en'):
    ret = {"data":[]}
    Attr = globals()[attr.title()]
    Attr_name = globals()[attr.title()+"_name"]
    join_id = "origin_id" if attr == "country" else attr+"_id"

    q = db.session.query(Attr, Attr_name) \
        .filter(Attr.id == getattr(Attr_name, join_id)) \
        .filter(Attr_name.lang == lang)
        # .filter(Attr.color!=None)
    # g.locale="en"
    # raise Exception(q.all()[100][0].get_abbrv())

    for attr, attr_name in q.all():
        attr = attr.serialize()
        attr["name"] = attr_name.name
        if hasattr(attr_name, "keywords"):
            attr["keywords"] = attr_name.keywords
        ret["data"].append(attr)

    ret = jsonify(ret)

    return ret

@mod.route('/palette/', methods = ['GET', 'POST'])
def palette():

    attrs = {"country": Country}

    if request.method == "POST":

        data = request.get_json()

        id = data.get("id", None)
        attr_type = data.get("attr_type", None)
        palette = data.get("palette", None)

        attr = attrs[attr_type].query.get(id)

        attr.palette = palette
        db.session.commit()

        return jsonify({"worked": True, "id": id})

    if request.is_xhr:

        for k, m in attrs.iteritems():
            attrs[k] = m.query.filter(m.image_link != None, m.palette == None).all()
            attrs[k] = [{"id": a.id, "image": a.get_image()} for a in attrs[k]]
        return jsonify(attrs=attrs)

    return render_template("scripts/palette.html")
