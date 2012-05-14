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

def country(request, country):
  s = time.time()
  # Find out what country the user is asking for
  try:
    c = Country.objects.get(name_3char=country)
  except Country.DoesNotExist:
    try:
      c = Country.objects.get(name_2char=country)
    except Country.DoesNotExist:
      return HttpResponse("Is that a new country? Never heard of it.")
  
  # Find out what this country's top exports are
  cpys = Hs4_cpy.objects.filter(country=c, year=2009, export_value__gt=0).order_by("-export_value")
  # exports = json.dumps([[x.product.name, x.export_value] for x in cpys])
  
  community_data = Hs4_cpy.objects.filter(country=c, year=2009).values_list("product__community__name", "product__community__color", "product__community__text_color").annotate(value=Sum('export_value'))
  
  # return page
  return render_to_response("overview/index.html", {
    "country": c,
    "community_data": json.dumps(list(community_data)),
    "cpys": cpys}, context_instance=RequestContext(request))