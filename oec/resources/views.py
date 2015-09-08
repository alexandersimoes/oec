# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template
from oec import app
from oec.general.views import get_locale

mod = Blueprint('resources', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","zh"):lang>/resources')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route("/data/")
def data():
    g.page_sub_type = "data"
    return render_template("resources/data.html")

@mod.route('/faqs/')
def faqs():
    g.page_sub_type = "faqs"
    return render_template("resources/faqs.html")
