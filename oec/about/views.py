# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template
from oec import app

mod = Blueprint('about', __name__, url_prefix='/about/')

@mod.before_request
def before_request():
    g.page_type = mod.name


###############################
# Legacy views (redirects)
# ---------------------------
@mod.route('api/')
@mod.route('api/embed/')
@mod.route('api/data/')
def api():
    return redirect(url_for("general.api"))

@mod.route('data/')
@mod.route('data/sources/')
@mod.route('data/download/')
def data_sources():
    return redirect(url_for('resources.data'))

@mod.route('permissions/')
def permissions():
    return redirect(url_for('general.permissions'))
