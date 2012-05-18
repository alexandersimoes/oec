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
  from collections import defaultdict
  
  year = int(year)
  min_year = 1964
  max_year = 2008 if category == "country" else 2009
  if year < min_year:
    return redirect('/rankings/%s/%d/' % (category, max_year))
  elif year > max_year:
    return redirect('/rankings/%s/%d/' % (category, min_year))
  
  rankings = defaultdict(dict)
  rankings_list = []
  
  if category == "country":
    year_rankings = Cy.objects.filter(year__in=[year, year-1]).values_list("eci_rank", "country__name_3char", "country__name_en", "eci", "year")
  elif category == "product":
    year_rankings = Sitc4_py.objects.filter(year__in=[year, year-1]).values_list("pci_rank", "product__code", "product__name_en", "pci", "year")
  
  for r in year_rankings:
    rankings[r[1]][r[4]] = r
  for r in rankings.values():
    if year-1 in r and year in r:
      rankings_list.append([r[year][0], r[year][1], r[year][2], r[year][3], r[year-1][0] - r[year][0]])
    elif year-1 not in r:
      rankings_list.append([r[year][0], r[year][1], r[year][2], r[year][3], 0])
  rankings_list.sort(key=lambda x: x[0])
  
  return render_to_response("rankings/index.html", {
    "category": category,
    "year": year,
    "rankings": rankings_list}, context_instance=RequestContext(request))