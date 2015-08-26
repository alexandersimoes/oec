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

@mod.route('/<attr>/')
@mod.route('/<attr>/<lang>/')
@crossdomain(origin='*')
def attrs(attr="country", lang='en'):
    ret = {"data":[]}
    data_classification = "hs92" if attr == "country" else attr
    data_models = getattr(db_data, "{}_models".format(data_classification))
    Attr = globals()[attr.title()]
    Attr_name = globals()[attr.title()+"_name"]
    Attr_data = data_models.Yo if attr == "country" else data_models.Yp
    join_id = "origin_id" if attr == "country" else attr+"_id"
    latest_year = available_years[data_classification][-1]
    
    # b1 = aliased(B)
    # b2 = aliased(B)
    # q = session.query(A.id, b1.id.label("b1_id"), b1.id.label("b2_id"))
    # q = q.outerjoin(b1, sqlalchemy.and_(A.id == b1.a_id, b1.c_id == 66))
    # q = q.outerjoin(b2, sqlalchemy.and_(A.id == b2.a_id, b2.c_id == 70))
    # q = q.filter(sqlalchemy.or_(b1.id != None, b2.id != None))

    # q = db.session.query(Attr, Attr_name, Attr_data) \
    #     .filter(Attr.id == getattr(Attr_name, join_id)) \
    #     .filter(Attr.id == getattr(Attr_data, join_id)) \
    #     .filter(Attr_data.year == latest_year) \
    #     .filter(Attr_name.lang == lang)
    # raise Exception(getattr(Attr_data, join_id), Attr_name.origin_id)
    
    q = db.session.query(Attr) \
        .outerjoin(Attr_data, and_(Attr.id == getattr(Attr_data, join_id), Attr_data.year == latest_year)) \
        .outerjoin(Attr_name, getattr(Attr_name, join_id) == Attr.id) \
        .add_entity(Attr_name) \
        .add_entity(Attr_data) \
        .filter(Attr_name.lang == lang)

    for attr, attr_name, attr_data in q.all():
        attr = attr.serialize()
        attr["name"] = attr_name.name
        attr["weight"] = attr_data.export_val if attr_data else None
        if hasattr(attr_name, "keywords"):
            attr["keywords"] = attr_name.keywords
        ret["data"].append(attr)

    ret = jsonify(ret)

    return ret

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
