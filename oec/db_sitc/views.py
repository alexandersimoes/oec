from flask import Blueprint, request, jsonify, make_response, g

from oec.utils import make_query
from oec.db_sitc.models import Yo, Yd, Yp, Yod, Yop, Ydp, Yodp
from oec.decorators import crossdomain

mod = Blueprint('sitc', __name__, url_prefix='/sitc')

@mod.after_request
def per_request_callbacks(response):
    if response.status_code != 302 and response.mimetype != "text/csv":
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<origin_id>/all/all/')
@mod.route('/<year>/<origin_id>/all/all/')
@crossdomain(origin='*')
def sitc_yo(**kwargs):
    return make_response(make_query(Yo, request.args, g.locale, **kwargs))

@mod.route('/all/all/<dest_id>/all/')
@mod.route('/<year>/all/<dest_id>/all/')
@crossdomain(origin='*')
def sitc_yd(**kwargs):
    return make_response(make_query(Yd, request.args, g.locale, **kwargs))

@mod.route('/all/all/all/<sitc_id>/')
@mod.route('/<year>/all/all/<sitc_id>/')
@crossdomain(origin='*')
def sitc_yp(**kwargs):
    return make_response(make_query(Yp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/show/all/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/all/')
@crossdomain(origin='*')
def sitc_yod(**kwargs):
    return make_response(make_query(Yod, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/all/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/all/show/')
@crossdomain(origin='*')
def sitc_yop(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/show/all/<sitc_id>/')
@mod.route('/<trade_flow>/<year>/show/all/<sitc_id>/')
@crossdomain(origin='*')
def sitc_yop_dest(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/<dest_id>/show/')
@crossdomain(origin='*')
def sitc_yodp(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/show/<sitc_id>/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/<sitc_id>/')
@crossdomain(origin='*')
def sitc_yodp_dest(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))