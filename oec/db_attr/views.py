from oec import db
from flask import Blueprint, request, jsonify, make_response, g
from oec.db_attr.models import Country, Country_name, Hs, Hs_name, Sitc, Sitc_name
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
        .filter(Attr_name.lang == lang) \
        .filter(Attr.color!=None)
    
    for attr, attr_name in q.all():
        attr = attr.serialize()
        attr["name"] = attr_name.name
        if hasattr(attr_name, "keywords"):
            attr["keywords"] = attr_name.keywords
        ret["data"].append(attr)
    
    ret = jsonify(ret)
    
    return ret