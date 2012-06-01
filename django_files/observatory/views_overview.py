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
    cpys = Hs4_cpy.objects.filter(country=c, year=2010, export_value__gt=0)
    total_value = cpys.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
    cpys = cpys.order_by("-export_value").values_list("product__community__id", "product__code", "product__name_en", "export_value")
    cpys = [[cpy[0], cpy[1], cpy[2], cpy[3], (cpy[3]/total_value)*100] for cpy in cpys]
  elif trade_flow == "import":
    cpys = Hs4_cpy.objects.filter(country=c, year=2010, import_value__gt=0)
    total_value = cpys.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
    cpys = cpys.order_by("-import_value").values_list("product__community__id", "product__code", "product__name_en", "import_value")
    cpys = [[cpy[0], cpy[1], cpy[2], cpy[3], (cpy[3]/total_value)*100] for cpy in cpys]
  else:
    return HttpResponse("Trade flow should be set to either export or import")
  # exports = json.dumps([[x.product.name, x.export_value] for x in cpys])
  # raise Exception(cpys)
  
  community_data = Hs4_cpy.objects.filter(country=c, year=2010).values_list("product__community__name", "product__community__color", "product__community__text_color").annotate(value=Sum('%s_value' % (trade_flow,)))
  
  items = Country.objects.filter(name_3char__isnull=False, region__isnull=False).order_by("name_en").values_list("name_en", "name_3char")
  
  # return page
  return render_to_response("overview/index.html", {
    "total_value": total_value,
    "country": c,
    "siblings": items,
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
    cpys = Hs4_cpy.objects.filter(product=p, year=2010, export_value__gt=0)
    total_value = cpys.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
    cpys = cpys.order_by("-export_value").values_list("country__name_3char", "country__name_3char", "country__name_en", "export_value")
    cpys = [[cpy[0], cpy[1], cpy[2], cpy[3], (cpy[3]/total_value)*100] for cpy in cpys]
  elif trade_flow == "import":
    cpys = Hs4_cpy.objects.filter(product=p, year=2010, import_value__gt=0)
    total_value = cpys.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
    cpys = cpys.order_by("-import_value").values_list("country__name_3char", "country__name_3char", "country__name_en", "import_value")
    cpys = [[cpy[0], cpy[1], cpy[2], cpy[3], (cpy[3]/total_value)*100] for cpy in cpys]
  else:
    return HttpResponse("Trade flow should be set to either export or import")
  
  community_data = Hs4_cpy.objects.filter(product=p, year=2010).values_list("country__region__name", "country__region__color", "country__region__text_color").annotate(value=Sum('%s_value' % (trade_flow,)))
  
  items = Hs4.objects.filter(ps_y__isnull=False).order_by("name_en").values_list("name_en", "code")
  
  # return page
  return render_to_response("overview/index.html", {
    "total_value": total_value,
    "product": p,
    "siblings": items,
    "trade_flow": trade_flow,
    "community_data": json.dumps(list(community_data)),
    "cpys": cpys}, context_instance=RequestContext(request))















def country2(request, country):
  s = time.time()
  # get country name based on url parameter
  c = clean_country(country)
  
  # get country ranking
  try:
    ranking = Cy.objects.get(year=2008, country=c)
    ranking_total = len(list(Cy.objects.filter(year=2008)))
  except Cy.DoesNotExist:
    ranking = None
    ranking_total = 128
  
  # get this country's exports
  export_products = get_products(c, "export")
  
  # get this country's imports
  import_products = get_products(c, "import")
  
  # get this country's export trade_partners
  export_countries = get_countries(c, "export")
  
  # get this country's import trade_partners
  import_countries = get_countries(c, "import")
  
  # get list of countries for dropdown
  country_list = Country.objects.filter(name_3char__isnull=False, region__isnull=False).order_by("name_en").values_list("name_en", "name_3char")
  
  return render_to_response("overview/country.html", {
    "country": c,
    "ranking": ranking,
    "ranking_total": ranking_total,
    "export_products": export_products,
    "export_countries": export_countries,
    "import_products": import_products,
    "import_countries": import_countries,
    "siblings": country_list}, context_instance=RequestContext(request))

def product(request, product):
  s = time.time()
  # get country name based on url parameter
  p = clean_product(product)
  
  # get country ranking
  try:
    ranking = Sitc4_py.objects.get(year=2009, product=p)
    ranking_total = len(list(Sitc4_py.objects.filter(year=2009)))
  except Sitc4_py.DoesNotExist:
    ranking = None
    ranking_total = 773
  
  # get this product's exporters
  export_countries = get_countries(p, "export")
  
  # get this product's importers
  import_countries = get_countries(p, "import")
  
  # get list of countries for dropdown
  if p.__class__ == Hs4:
    product_list = Hs4.objects.filter(code__isnull=False).order_by("name_en").values_list("name_en", "code")
  else:
    product_list = Sitc4.objects.filter(code__isnull=False).order_by("name_en").values_list("name_en", "code")
  
  return render_to_response("overview/product.html", {
    "product": p,
    "ranking": ranking,
    "ranking_total": ranking_total,
    "export_countries": export_countries,
    "import_countries": import_countries,
    "siblings": product_list}, context_instance=RequestContext(request))

def clean_country(country):
  # first try looking up based on 3 character code
  try:
    c = Country.objects.get(name_3char=country)
  except Country.DoesNotExist:
    # next try 2 character code
    try:
      c = Country.objects.get(name_2char=country)
    except Country.DoesNotExist:
      c = None
  return c

def clean_product(product):
  # first try looking up based on 3 character code
  try:
    p = Hs4.objects.get(code=product)
  except Hs4.DoesNotExist:
    # next try SITC4
    try:
      p = Sitc4.objects.get(code=product)
    except Sitc4.DoesNotExist:
      p = None
  return p

def get_products(c, trade_flow):
  prods = Hs4_cpy.objects.filter(country=c, year=2010)
  total_value = prods.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
  prods = prods.values_list("product__community__id", "product__community__name", "product__code", "product__name_en", "%s_value" % (trade_flow,))
  prods = [[p[0], p[1], p[2], p[3], p[4], (p[4]/total_value)*100] for p in prods if p[4] > 0]
  prods.sort(key=lambda x: x[4], reverse=True)
  return prods

def get_countries(input, trade_flow):
  if input.__class__ == Country:
    countries = Hs4_ccpy.objects.filter(origin=input, year=2010).values_list("destination__name_3char", "destination__name_en").annotate(value=Sum('%s_value'%(trade_flow,)))
    total_value = sum([c[2] for c in countries])
    countries = [[c[0], c[1], c[2], (c[2]/total_value)*100] for c in countries if c[2] > 0]
    countries.sort(key=lambda c: c[2], reverse=True)
  else:
    if input.__class__ == Hs4:
      countries = Hs4_cpy.objects.filter(product=input, year=2010)
    else:
      countries = Sitc4_cpy.objects.filter(product=input, year=2009).exclude(country=231)
    total_value = countries.aggregate(Sum("%s_value" % (trade_flow))).values()[0]
    countries = countries.values_list("country__region__id", "country__region__name", "country__name_3char", "country__name_en", "%s_value" % (trade_flow,))
    countries = [[c[0], c[1], c[2], c[3], c[4], (c[4]/total_value)*100] for c in countries if c[4] > 0]
    countries.sort(key=lambda x: x[4], reverse=True)
  return countries