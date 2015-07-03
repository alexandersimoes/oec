# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template
from oec import app

mod = Blueprint('resources', __name__, url_prefix='/resources/')

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route("publications/")
def publications():
    g.page_sub_type = "publications"
    return render_template("resources/publications.html")
