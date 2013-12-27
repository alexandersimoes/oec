from flask import Blueprint, request, jsonify, make_response, g
from oec.utils import gzip_data, cached_query
from oec.db_attr.models import Country, Hs, Sitc

mod = Blueprint('attr', __name__, url_prefix='/attr')

@mod.after_request
def per_request_callbacks(response):
    if response.status_code != 302 and response.mimetype != "text/csv":
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

############################################################
# ----------------------------------------------------------
# All attribute views
# 
############################################################

@mod.route('/<attr>/')
@mod.route('/<attr>/<Attr_id>/')
def attrs(attr="country", Attr_id=None):
    ret = {}
    lang = request.args.get('lang', None) or g.locale
    Attr = globals()[attr.title()]
    cache_id = request.path + lang
    
    # first lets test if this query is cached
    cached_q = cached_query(cache_id)
    if cached_q:
        ret = make_response(cached_q)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))
        return ret
    
    attrs = Attr.query.filter(Hs.color!=None).all()
    
    ret["data"] = [a.serialize() for a in attrs]
    
    ret = jsonify(ret)
    ret.data = gzip_data(ret.data)

    if cached_q is None:
        cached_query(cache_id, ret.data)
        
    ret.headers['Content-Encoding'] = 'gzip'
    ret.headers['Content-Length'] = str(len(ret.data))
    
    return ret