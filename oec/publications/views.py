# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template
from oec import app
from oec.general.views import get_locale

mod = Blueprint('publications', __name__, url_prefix='/<any("ar","de","el","en","es","fr","he","hi","it","ja","ko","mn","nl","ru","pt","tr","zh"):lang>/publications')

@mod.url_value_preprocessor
def get_profile_owner(endpoint, values):
    lang = values.pop('lang')
    g.locale = get_locale(lang)

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route("/books/")
def books():
    g.page_sub_type = "books"
    return render_template("publications/books.html")

@mod.route("/papers/")
def papers():
    g.page_sub_type = "papers"
    return render_template("publications/papers.html")
