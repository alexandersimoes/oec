from flask import Blueprint, request, jsonify, make_response, g

from oec.utils import make_query
# from oec.db_hs.models import Yo, Yd, Yp, Yod, Yop, Ydp, Yodp

mod = Blueprint('hs', __name__, url_prefix='/hs')

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<origin_id>/all/all/')
@mod.route('/<year>/<origin_id>/all/all/')
def hs_yo(**kwargs):
    return make_response(make_query(Yo, request.args, g.locale, **kwargs))

@mod.route('/all/all/<dest_id>/all/')
@mod.route('/<year>/all/<dest_id>/all/')
def hs_yd(**kwargs):
    return make_response(make_query(Yd, request.args, g.locale, **kwargs))

@mod.route('/all/all/all/<hs_id>/')
@mod.route('/<year>/all/all/<hs_id>/')
def hs_yp(**kwargs):
    return make_response(make_query(Yp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<dest_id>/all/')
@mod.route('/<year>/<origin_id>/<dest_id>/all/')
def hs_yod(**kwargs):
    return make_response(make_query(Yod, request.args, g.locale, **kwargs))

@mod.route('/all/<origin_id>/all/<hs_id>/')
@mod.route('/<year>/<origin_id>/all/<hs_id>/')
def hs_yop(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

@mod.route('/all/all/<dest_id>/<hs_id>/')
@mod.route('/<year>/all/<dest_id>/<hs_id>/')
def hs_ydp(**kwargs):
    return make_response(make_query(Ydp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<dest_id>/<hs_id>/')
@mod.route('/<year>/<origin_id>/<dest_id>/<hs_id>/')
def hs_yodp(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))