from flask import Blueprint, request, jsonify, make_response, g

from oec import db
from oec.utils import make_query
from oec.db_attr.models import Yo as Attr_yo
from oec.db_data import hs92_models
from oec.db_data import hs96_models
from oec.db_data import hs02_models
from oec.db_data import hs07_models
from oec.db_data import sitc_models
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
    elif classification == "sitc":
        g.prod_models = sitc_models
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
def yo(**kwargs):
    q = db.session.query(Attr_yo, getattr(g.prod_models, "Yo")) \
            .filter(Attr_yo.origin_id == getattr(g.prod_models, "Yo").origin_id) \
            .filter(Attr_yo.year == getattr(g.prod_models, "Yo").year)
    return make_response(make_query(q, request.args, g.locale, getattr(g.prod_models, "Yo"), **kwargs))

@mod.route('/<trade_flow>/all/all/<dest_id>/all/')
@mod.route('/<trade_flow>/all/wld/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/all/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/all/show/all/')
@mod.route('/<trade_flow>/<year>/wld/show/all/')
@crossdomain(origin='*')
def yd(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yd"), request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/all/all/<prod_id>/')
@mod.route('/<trade_flow>/all/wld/all/show/')
@mod.route('/<trade_flow>/<year>/all/all/<prod_id>/')
@mod.route('/<trade_flow>/<year>/all/all/show/')
@mod.route('/<trade_flow>/<year>/wld/all/show/')
@crossdomain(origin='*')
def yp(**kwargs):
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
def yod(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yod"), request.args, g.locale, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/all/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/all/show/')
@crossdomain(origin='*')
def yop(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yop"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

@mod.route('/<trade_flow>/all/show/all/<prod_id>/')
@mod.route('/<trade_flow>/<year>/show/all/<prod_id>/')
@crossdomain(origin='*')
def yop_dest(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yop"), \
        request.args, g.locale, classification=g.prod_classification, **kwargs))

@mod.route('/<trade_flow>/all/all/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/all/<dest_id>/show/')
@mod.route('/<trade_flow>/all/wld/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/wld/<dest_id>/show/')
@crossdomain(origin='*')
def ydp(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Ydp"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

@mod.route('/<trade_flow>/all/all/show/<prod_id>/')
@mod.route('/<trade_flow>/<year>/all/show/<prod_id>/')
@mod.route('/<trade_flow>/all/wld/show/<prod_id>/')
@mod.route('/<trade_flow>/<year>/wld/show/<prod_id>/')
@crossdomain(origin='*')
def ydp_dest(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Ydp"), \
        request.args, g.locale, classification=g.prod_classification, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/<trade_flow>/all/<origin_id>/<dest_id>/all/')
@mod.route('/<trade_flow>/<year>/<origin_id>/<dest_id>/all/')
@mod.route('/<trade_flow>/all/<origin_id>/<dest_id>/show/')
@mod.route('/<trade_flow>/<year>/<origin_id>/<dest_id>/show/')
@crossdomain(origin='*')
def yodp(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yodp"), \
        request.args, g.locale, classification=g.prod_classification, \
        output_depth=g.output_depth, **kwargs))

@mod.route('/<trade_flow>/all/<origin_id>/show/<prod_id>/')
@mod.route('/<trade_flow>/<year>/<origin_id>/show/<prod_id>/')
@crossdomain(origin='*')
def yodp_dest(**kwargs):
    return make_response(make_query(getattr(g.prod_models, "Yodp"), \
        request.args, g.locale, classification=g.prod_classification, **kwargs))