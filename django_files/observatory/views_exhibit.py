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

def api_near(request, country, year, num_prods):
  c = Country.objects.get(name_3char=country) # The country
  y = int(year) # The year
  to_show = int(num_prods) # The number of products to get data for
  
  # Need to use NumPy library for matrix calculations
  import numpy as np
  import operator # Use this for sorting list of tuples by second value
  density_data = {}
  ##################################################
  # Get list of countries for this year
  cpys = Hs4_cpy.objects.filter(year=y, product__ps_x__isnull=False)
  # Many calculations are determinate on which countries and which products
  # are included in the dataset used. Here we are using all countries
  # or products that appear in the original Product Space
  distinct_countries = cpys.values_list('country', flat=True).distinct()
  distinct_products = cpys.values_list('product', flat=True).distinct()
  # Matricies rely on knowing which row and column a particular country
  # or product is in thus we need to create a dictionary giving us the
  # ability to look up countries and products by their IDs
  country_matrix = {}
  matrix_country = {} # provides reverse lookup
  prod_matrix = {}
  matrix_prod = {}
  for i, country_id in enumerate(distinct_countries):
    country_matrix[country_id] = i
    matrix_country[i] = country_id
  for i, prod_id in enumerate(distinct_products):
    prod_matrix[prod_id] = i
    matrix_prod[i] = prod_id
  # Create an all Zeros matrix with the proper number of rows and columns
  # mpc = matrix of products and countries
  mpc = np.zeros(shape = (len(distinct_products), len(distinct_countries)))
  # Create adjacency matrix for products x countries
  # i.e. 1 if product exported with RCA > 1 | 0 otherwise
  cpys_rca_greater1 = cpys.filter(rca__gte=1)
  for cpy in cpys_rca_greater1:
    # Matrix cells are accessed via (row, column)
    mpc[prod_matrix[cpy.product_id], country_matrix[cpy.country_id]] = 1
  # Print number of rows and columns
  # raise Exception(mpc.shape)
  #
  # Transpose MPC matrix so it is now MCP matrix ie switch 
  # countries with products
  mpc_trans = mpc.transpose()
  # Matrix multiplication on mpc matrix and transposed version,
  # number of products = number of rows and vice versa on transposed
  # version, thus the shape of this result will be length of products by
  # by the length of products (symetric)
  numerator_intersection = np.dot(mpc, mpc_trans)
  # kp0 is a vector of the sums of the intersections
  # raise Exception(len(np.array(kp0)[0])) #length should be the num of prods
  kp0 = np.matrix(mpc.sum(axis=1))
  # transpose this to get the unions
  kp0_trans = np.matrix(kp0.transpose())
  # multiply these two vectors as matricies, take the squre root
  # and then we have the denominator
  denominator_union = np.dot(kp0_trans, kp0)
  denominator_union_sqrt = np.power(denominator_union, .5)
  # to get the proximities it is now a simple division of 2 matricies
  proximities = np.true_divide(numerator_intersection, denominator_union_sqrt)
  proximities = np.nan_to_num(proximities)
  ## TODO: gets 0s here fix that (maybe fixed see above) 
  # Get numerator by matrix multiplication of proximities with mpc
  density_numerator = np.dot(proximities, mpc)
  # Get denominator by multiplying proximities by all ones vector thus
  # getting the sum of all proximities
  ones_matrix = np.ones_like(mpc)
  density_denominator = np.dot(proximities, ones_matrix)
  # We now have our densities matrix by dividing numerator by denomiator
  densities = np.true_divide(density_numerator, density_denominator)
  prods_not_exported = Hs4_cpy.objects.filter(country=c, year=y, rca__lt=1, product__ps_x__isnull=False).values_list('product', flat=True)
  # raise Exception(this_country_not_exports_values)
  # raise Exception(len(np.array(densities[:,c_dict[country.id]].flatten(1))[0]))
  closest_product_rows = []
  for i, density in enumerate(np.array(densities[:,country_matrix[c.id]].flatten(1))[0]):
    if matrix_prod[i] in prods_not_exported:
      # closest_product_rows.append((density, i))
      closest_product_rows.append((density, matrix_prod[i]))
  # Sort from highest to lowest the products with the highest density values
  # that are NOT exported by this country
  closest_product_rows = sorted(closest_product_rows, reverse=True)
  return HttpResponse(json.dumps(closest_product_rows[:int(to_show)]))
  """
  density_data = []
  for density_prow in closest_product_rows[:int(to_show)]:
    # Get product from the database that we are currently dealing with
    p_row = density_prow[1]
    product = Sitc4.objects.get(pk=matrix_prod[p_row])
    deltas = []
    # Loop through each density value in the row for this product and subtract
    # their density value by our countries to get the difference (which we
    # will then sort by to get the closest countries)
    for i, density in enumerate(np.array(densities[p_row]).flatten()):
      # Get country fron DB
      country_name = Country.objects.get(pk=matrix_country[i]).name
      diff = abs(density_prow[0] - density)
      deltas.append((diff, density, country_name, product.name, product.leamer.color))
    # First sort by the difference (which is closest to our country)
    deltas.sort()
    # Now take the top 5 and sort by actual density value
    deltas = sorted(deltas[:5], key=operator.itemgetter(1), reverse=True)
    density_data.append(deltas)
  # raise Exception(density_data)
  return HttpResponse(json.dumps({"this_country":c.name, "density_data": density_data}))
  """