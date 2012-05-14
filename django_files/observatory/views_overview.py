# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.urlresolvers import resolve
# General
import json
# Project specific
from django.utils.translation import gettext as _
# App specific
from observatory.models import *
import time

def country(request, country, trade_flow="export"):
  
  # Find out what country the user is asking for
  try:
    c = Country.objects.get(name_3char=country)
  except Country.DoesNotExist:
    try:
      c = Country.objects.get(name_2char=country)
    except Country.DoesNotExist:
      return HttpResponse("Is that a new country? Never heard of it.")
  
  # Find out what this country's top exports are
  if trade_flow == "export":
    cpys = Hs4_cpy.objects.filter(country=c, year=2010, export_value__gt=0).order_by("-export_value").values_list("product__community__id", "product__code", "product__name_en", "export_value")
  elif trade_flow == "import":
    cpys = Hs4_cpy.objects.filter(country=c, year=2010, import_value__gt=0).order_by("-import_value").values_list("product__community__id", "product__code", "product__name_en", "import_value")
  else:
    return HttpResponse("Trade flow should be set to either export or import")
  # exports = json.dumps([[x.product.name, x.export_value] for x in cpys])
  # raise Exception(cpys)
  
  community_data = Hs4_cpy.objects.filter(country=c, year=2010).values_list("product__community__name", "product__community__color", "product__community__text_color").annotate(value=Sum('%s_value' % (trade_flow,)))
  
  # return page
  return render_to_response("overview/index.html", {
    "country": c,
    "trade_flow": trade_flow,
    "community_data": json.dumps(list(community_data)),
    "cpys": cpys}, context_instance=RequestContext(request))

def product(request, product, trade_flow="export"):
  
  # Find out what country the user is asking for
  try:
    p = Hs4.objects.get(code=product)
  except Hs4.DoesNotExist:
    return HttpResponse("Is that a new product? Never heard of it.")
  
  # Find out what this country's top exports are
  if trade_flow == "export":
    cpys = Hs4_cpy.objects.filter(product=p, year=2010, export_value__gt=0).order_by("-export_value").values_list("country__name_3char", "country__name_3char", "country__name_en", "export_value")
  elif trade_flow == "import":
    cpys = Hs4_cpy.objects.filter(product=p, year=2010, import_value__gt=0).order_by("-import_value").values_list("country__name_3char", "country__name_3char", "country__name_en", "import_value")
  else:
    return HttpResponse("Trade flow should be set to either export or import")
  # exports = json.dumps([[x.product.name, x.export_value] for x in cpys])
  # raise Exception(cpys)
  
  community_data = Hs4_cpy.objects.filter(product=p, year=2010).values_list("country__region__name", "country__region__color", "country__region__text_color").annotate(value=Sum('%s_value' % (trade_flow,)))
  
  # return page
  return render_to_response("overview/index.html", {
    "product": p,
    "trade_flow": trade_flow,
    "community_data": json.dumps(list(community_data)),
    "cpys": cpys}, context_instance=RequestContext(request))