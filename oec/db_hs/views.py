from flask import Blueprint, request, jsonify, make_response, g

from oec.utils import make_query
from oec.db_hs.models import Yo, Yd, Yp, Yod, Yop, Ydp, Yodp

mod = Blueprint('hs', __name__, url_prefix='/hs')

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<origin_id>/all/all/')
@mod.route('/<year>/<origin_id>/all/all/')
def rais_yb(**kwargs):
    return make_response(make_query(Yo, request.args, g.locale, **kwargs))

@mod.route('/all/all/<destination_id>/all/')
@mod.route('/<year>/all/<destination_id>/all/')
def rais_yi(**kwargs):
    return make_response(make_query(Yd, request.args, g.locale, **kwargs))

@mod.route('/all/all/all/<hs_id>/')
@mod.route('/<year>/all/all/<hs_id>/')
def rais_yo(**kwargs):
    return make_response(make_query(Yp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<destination_id>/all/')
@mod.route('/<year>/<origin_id>/<destination_id>/all/')
def rais_ybi(**kwargs):
    return make_response(make_query(Yod, request.args, g.locale, **kwargs))

@mod.route('/all/<origin_id>/all/<hs_id>/')
@mod.route('/<year>/<origin_id>/all/<hs_id>/')
def rais_ybo(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

@mod.route('/all/all/<destination_id>/<hs_id>/')
@mod.route('/<year>/all/<destination_id>/<hs_id>/')
def rais_yio(**kwargs):
    return make_response(make_query(Ydp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<destination_id>/<hs_id>/')
@mod.route('/<year>/<origin_id>/<destination_id>/<hs_id>/')
def rais_ybio(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))