from flask import Blueprint, request, jsonify, make_response, g

from oec.utils import make_query
from oec.db_sitc.models import Yo, Yd, Yp, Yod, Yop, Ydp, Yodp

mod = Blueprint('sitc', __name__, url_prefix='/sitc')

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<origin_id>/all/all/')
@mod.route('/<year>/<origin_id>/all/all/')
def sitc_yo(**kwargs):
    return make_response(make_query(Yo, request.args, g.locale, **kwargs))

@mod.route('/all/all/<destination_id>/all/')
@mod.route('/<year>/all/<destination_id>/all/')
def sitc_yd(**kwargs):
    return make_response(make_query(Yd, request.args, g.locale, **kwargs))

@mod.route('/all/all/all/<sitc_id>/')
@mod.route('/<year>/all/all/<sitc_id>/')
def sitc_yp(**kwargs):
    return make_response(make_query(Yp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<destination_id>/all/')
@mod.route('/<year>/<origin_id>/<destination_id>/all/')
def sitc_yod(**kwargs):
    return make_response(make_query(Yod, request.args, g.locale, **kwargs))

@mod.route('/all/<origin_id>/all/<sitc_id>/')
@mod.route('/<year>/<origin_id>/all/<sitc_id>/')
def sitc_yop(**kwargs):
    return make_response(make_query(Yop, request.args, g.locale, **kwargs))

@mod.route('/all/all/<destination_id>/<sitc_id>/')
@mod.route('/<year>/all/<destination_id>/<sitc_id>/')
def sitc_ydp(**kwargs):
    return make_response(make_query(Ydp, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<origin_id>/<destination_id>/<sitc_id>/')
@mod.route('/<year>/<origin_id>/<destination_id>/<sitc_id>/')
def sitc_yodp(**kwargs):
    return make_response(make_query(Yodp, request.args, g.locale, **kwargs))