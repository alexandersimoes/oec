from flask import Blueprint, request, jsonify, make_response, g

from oec import db
from oec.utils import make_query
from oec.db_attr.models import Yo as Attr_yo
from oec.db_hs.models import Yo, Yd, Yp, Yod, Yop, Ydp, Yodp
from oec.decorators import crossdomain

mod = Blueprint('hs', __name__, url_prefix='/hs')

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/all/all/')
@mod.route('/<trade_flow>/<year>/<origin_id>/all/all/')
@mod.route('/<trade_flow>/<year>/show/all/all/')
@crossdomain(origin='*')
def hs_yo(**kwargs):
    q = db.session.query(Attr_yo, Yo) \
            .filter(Attr_yo.origin_id == Yo.origin_id) \
            .filter(Attr_yo.year == Yo.year)
    return make_response(make_query(q, request.args, g.locale, Yo, **kwargs))

@mod.route('/<trade_flow>/all/all/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/all/<dest_id>/all/')
@crossdomain(origin='*')
def hs_yd(**kwargs):
    return make_response(make_query(Yd, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/all/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/all/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/all/all/show/')
@crossdomain(origin='*')
def hs_yp(**kwargs):
    return make_response(make_query(Yp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/show/all/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/all/')
@crossdomain(origin='*')
def hs_yod(**kwargs):
    return make_response(make_query(Yod, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/all/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/all/show/')
@crossdomain(origin='*')
def hs_yop(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/show/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/show/all/<hs_id>/')
@crossdomain(origin='*')
def hs_yop_dest(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/<dest_id>/show/')
@crossdomain(origin='*')
def hs_yodp(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/show/<hs_id>/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/<hs_id>/')
@crossdomain(origin='*')
def hs_yodp_dest(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))