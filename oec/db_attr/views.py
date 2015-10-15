from sqlalchemy import and_
from oec import db, db_data, available_years
from flask import Blueprint, request, jsonify, make_response, g, render_template
from oec.db_attr.models import *
from oec.decorators import crossdomain

mod = Blueprint('attr', __name__, url_prefix='/attr')

############################################################
# ----------------------------------------------------------
# All attribute views
#
############################################################

@mod.route('/eci/')
@crossdomain(origin='*')
def eci():
    countries = Yo.query.filter(Yo.eci != None).all()
    return jsonify(data=[c.serialize() for c in countries])

@mod.route('/<attr>/')
@mod.route('/<attr>/<lang>/')
@crossdomain(origin='*')
def attrs(attr="country", lang='en'):
    attrs = []
    data_classification = "hs92" if attr == "country" else attr
    data_models = getattr(db_data, "{}_models".format(data_classification))
    Attr = globals()[attr.title()]
    Attr_name = globals()[attr.title()+"_name"]
    Attr_data = data_models.Yo if attr == "country" else data_models.Yp
    join_id = "origin_id" if attr == "country" else attr+"_id"
    latest_year = available_years[data_classification][-1]
    
    q = db.session.query(Attr) \
        .outerjoin(Attr_data, and_(Attr.id == getattr(Attr_data, join_id), Attr_data.year == latest_year)) \
        .outerjoin(Attr_name, getattr(Attr_name, join_id) == Attr.id) \
        .add_entity(Attr_name) \
        .add_entity(Attr_data) \
        .filter(Attr_name.lang == lang)
    
    total_weight = sum(filter(None, [a[2].export_val for a in q.all() if a[2]]))

    for attr, attr_name, attr_data in q.all():
        attr = attr.serialize()
        attr["name"] = attr_name.name
        if attr_data:
            attr["weight"] = attr_data.export_val
        if attr["id"] == "xxwld":
            attr["weight"] = total_weight
        if hasattr(attr_name, "keywords"):
            attr["keywords"] = attr_name.keywords
        attrs.append(attr)

    return jsonify(data=attrs)

@mod.route('/palette/', methods = ['GET', 'POST'])
def palette():

    attrs = {"country": Country, "hs": Hs92}

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
