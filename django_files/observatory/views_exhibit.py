# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
# General
import json
# Project specific
from django.utils.translation import gettext as _
# App specific
from observatory.models import *

def index(request, category="country", year=2008):
  return render_to_response("exhibit/index.html")

def country_selection(request):
  return render_to_response("exhibit/country_selection.html")
def product_selection(request):
  return render_to_response("exhibit/product_selection.html")
def year_selection(request):
  return render_to_response("exhibit/year_selection.html")