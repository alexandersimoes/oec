from flask import Blueprint, request, jsonify, make_response, g
from oec.db_attr.models import Country, Hs, Sitc
from oec.decorators import crossdomain

mod = Blueprint('attr', __name__, url_prefix='/attr')

############################################################
# ----------------------------------------------------------
# All attribute views
# 
############################################################

@mod.route('/<attr>/')
@mod.route('/<attr>/<Attr_id>/')
@crossdomain(origin='*')
def attrs(attr="country", Attr_id=None):
    ret = {}
    lang = request.args.get('lang', None) or g.locale
    Attr = globals()[attr.title()]
    
    attrs = Attr.query.filter(Attr.color!=None).all()
    # attrs = Attr.query.all()
    # raise Exception(attrs)
    ret["data"] = [a.serialize() for a in attrs]
    
    ret = jsonify(ret)
    
    return ret