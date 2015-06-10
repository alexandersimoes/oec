from flask import Blueprint, request, jsonify, make_response, g

from oec import db
from oec.utils import make_query
from oec.db_attr.models import Yo as Attr_yo
from oec.db_data import hs92_models
from oec.db_data import hs96_models
from oec.db_data import hs02_models
from oec.db_data import hs07_models
from oec.decorators import crossdomain

mod = Blueprint('data', __name__, url_prefix='/<any("sitc","hs","hs92","hs96","hs02","hs07"):classification>')

@mod.url_value_preprocessor
def get_product_classification_models(endpoint, values):
    g.locale="en"
    classification = values.pop('classification')
    g.prod_classification = classification
    if classification == "hs" or classification == "hs92":
        g.prod_models = hs92_models
    elif classification == "hs96":
        g.prod_models = hs96_models
    elif classification == "hs02":
        g.prod_models = hs02_models
    elif classification == "hs07":
        g.prod_models = hs07_models
    g.output_depth = request.args.get("output_depth")

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
    q = db.session.query(Attr_yo, getattr(g.prod_models, "Yo")) \
            .filter(Attr_yo.origin_id == getattr(g.prod_models, "Yo").origin_id) \
            .filter(Attr_yo.year == getattr(g.prod_models, "Yo").year)
    return make_response(make_query(q, request.args, g.locale, getattr(g.prod_models, "Yo"), **kwargs))

@mod.route('/<trade_flow>/all/all/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/all/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/all/show/all/')
@crossdomain(origin='*')
def hs_yd(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yd"), request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/all/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/all/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/all/all/show/')
@crossdomain(origin='*')
def hs_yp(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yp"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/show/all/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/all/')
@crossdomain(origin='*')
def hs_yod(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yod"), request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/all/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/all/show/')
@crossdomain(origin='*')
def hs_yop(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yop"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

@mod.route('/<trade_flow>/all/show/all/<hs_id>/')
@mod.route('/<trade_flow>/<year>/show/all/<hs_id>/')
@crossdomain(origin='*')
def hs_yop_dest(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yop"), \
        request.args, g.locale, classification=g.prod_classification, **kwargs))

@mod.route('/<trade_flow>/all/all/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/all/<dest_id>/show/')
@crossdomain(origin='*')
def hs_ydp(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Ydp"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/<dest_id>/show/')
@crossdomain(origin='*')
def hs_yodp(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yodp"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/show/<hs_id>/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/<hs_id>/')
@crossdomain(origin='*')
def hs_yodp_dest(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yodp"), \
        request.args, g.locale, classification=g.prod_classification, **kwargs))