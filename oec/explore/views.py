from werkzeug.routing import ValidationError, BaseConverter
from flask import Blueprint, g, redirect, url_for
from oec import app, available_years
from oec.general.views import get_locale

class YearConverter(BaseConverter):
    all_years = [item for sublist in available_years.values() for item in sublist]
    min_year = min(all_years)
    max_year = max(all_years)

    def to_python(self, value):

        '''force int conversion'''
        try:
            years = [int(y) for y in value.split('.')]
        except ValueError:
            raise ValidationError()

        '''treat as range'''
        if len(years) == 2:
            years = range(years[0], years[1]+1)
        elif len(years) > 2:
            years = range(years[0], years[1]+1, years[2])

        '''clamp years based on min/max available years for all classifications'''
        try:
            clamped_min = years.index(self.min_year)
        except ValueError:
            clamped_min = 0
        try:
            clamped_max = years.index(self.max_year)
        except ValueError:
            clamped_max = len(years)-1

        return years

    def to_url(self, values):
        return '.'.join(str(value) for value in values)

app.url_map.converters['year'] = YearConverter

@app.route('/explore/')
@app.route('/explore/<app_name>/')
@app.route('/explore/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def explore_redirect_nolang(app_name=None, classification=None, trade_flow=None, \
                origin_id=None, dest_id=None, prod_id=None, year=None):
    year = year or available_years["hs92"][-1]
    if classification:
        redirect_url = url_for('visualize.visualize', lang=g.locale, app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year)
    elif app_name:
        redirect_url = url_for('visualize.visualize_redirect', lang=g.locale, app_name=app_name)
    else:
        redirect_url = url_for('visualize.visualize_redirect', lang=g.locale)
    return redirect(redirect_url)

@app.route('/explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@app.route('/explore/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def embed_redirect_nolang(app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year=None):
    year = year or available_years[classification][-1]
    return redirect(url_for('visualize.embed', lang=g.locale, app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year))

mod = Blueprint('explore', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","zh"):lang>/explore')
@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.route('/')
@mod.route('/<app_name>/')
def explore_redirect(app_name='tree_map'):
    return redirect(url_for('visualize.visualize_redirect', lang=g.locale, app_name=app_name))

@mod.route('/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def explore(app_name, classification, trade_flow, origin_id, dest_id, prod_id, year=None):
    redirect_url = url_for('visualize.visualize', lang=g.locale, app_name=app_name, \
                    classification=classification, trade_flow=trade_flow, \
                    origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                    year=year)
    return redirect(redirect_url)

@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/')
@mod.route('/embed/<app_name>/<classification>/<trade_flow>/<origin_id>/<dest_id>/<prod_id>/<year:year>/')
def embed(app_name, classification, trade_flow, origin_id, dest_id, \
                prod_id, year=available_years['hs92'][-1]):
    return redirect(url_for('visualize.embed', lang=g.locale, app_name=app_name, \
                        classification=classification, trade_flow=trade_flow, \
                        origin_id=origin_id, dest_id=dest_id, prod_id=prod_id, \
                        year=year))

