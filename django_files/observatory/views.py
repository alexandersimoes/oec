# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
# General
import json
# Project specific
from atlas.languages import supported_langs
# App specific
from observatory.models import *

def home(request):
	try:
		ip = request.META["HTTP_X_FORWARDED_FOR"]
	except KeyError:
		ip = request.META["REMOTE_ADDR"]
	return render_to_response("home.html", {"client_ip": ip, "supported_langs": supported_langs})

def about(request):
	return render_to_response("about/index.html", {"supported_langs": supported_langs})
def team(request):
	return render_to_response("about/team.html", {"supported_langs": supported_langs})

def api(request):
	return render_to_response("api/index.html", {"supported_langs": supported_langs})

def book(request):
	return render_to_response("book/index.html", {"supported_langs": supported_langs})


def app(request, app_name, trade_flow, filter, year):
	# Get URL query parameters
	format = request.GET.get("format", False)
	lang = request.GET.get("lang", False)
	crawler = request.GET.get("_escaped_fragment_", False)
	
	country1, country2, product = None, None, None
	country1_list, country2_list, product_list, year1_list, year2_list, year_interval_list, year_interval = None, None, None, None, None, None, None
	
	trade_flow_list = ["export", "import", "net_export", "net_import"]
	
	year1_list = range(1962, 2010, 1)
	if "." in year:
		y = [int(x) for x in year.split(".")]
		year = range(y[0], y[1]+1, y[2])
		year2_list = year1_list
		year_interval_list = range(1, 11)
		year_interval = year[1] - year[0]
	else:
		year = int(year)
	
	json_response = {
		"year": year,
		"app": app_name
	}
	
	# Bilateral
	if "." in filter:
		bilateral_filters = filter.split(".")
		
		# Country x Product
		if len(bilateral_filters[1]) > 3:
			country1 = Country.objects.get(name_3char=bilateral_filters[0])
			product = Sitc4.objects.get(code=bilateral_filters[1])
			country1_list = Country.objects.get_all(lang)
			product_list = Sitc4.objects.get_all(lang)
			
			article = "to" if trade_flow == "export" else "from"
			title = "Where does %s %s %s %s?" % (country1.name, trade_flow, product.name_en, article)
			
			# cspy means country1 / countr2 / show / year
			if crawler == "" or format == "json":
				json_response["data"] = Sitc4_ccpy.objects.cspy(country1, product, trade_flow)
				json_response["attr_data"] = Country.objects.get_all(lang)
				json_response["title"] = title
			
		# Country x Country
		else:
			country1 = Country.objects.get(name_3char=bilateral_filters[0])
			country2 = Country.objects.get(name_3char=bilateral_filters[1])
			country1_list = Country.objects.get_all(lang)
			country2_list = country1_list
			
			article = "to" if trade_flow == "export" else "from"
			title = "What does %s %s %s %s?" % (country1.name, trade_flow, article, country2.name)
			
			# ccsy means country1 / countr2 / show / year
			if crawler == "" or format == "json":
				json_response["data"] = Sitc4_ccpy.objects.ccsy(country1, country2, trade_flow)
				json_response["attr_data"] = Sitc4.objects.get_all(lang)
				json_response["title"] = title
	
	# Product
	elif len(filter) > 3:
		product = Sitc4.objects.get(code=filter)
		product_list = Sitc4.objects.get_all(lang)
				
		title = "Who %ss %s?" % (trade_flow, product.name_en)
		
		# sapy means show / all / product / year
		if crawler == "" or format == "json":
			json_response["data"] = Sitc4_cpy.objects.sapy(product, trade_flow)
			json_response["attr_data"] = Country.objects.get_all(lang)
			json_response["title"] = title
	
	# Country
	else:
		country1 = Country.objects.get(name_3char=filter)
		country1_list = Country.objects.get_all(lang)
		
		title = "What does %s %s?" % (country1.name, trade_flow)
		
		# casy means country1 / all / show / year
		if crawler == "" or format == "json":
			json_response["data"] = Sitc4_cpy.objects.casy(country1, trade_flow)
			json_response["attr_data"] = Sitc4.objects.get_all(lang)
			json_response["title"] = title
	
	# Send data as JSON to browser via AJAX
	if format == "json":
		return HttpResponse(json.dumps(json_response))
	
	# Return page without visualization data
	return render_to_response("app/index.html", {
		"supported_langs": supported_langs,
		"title": title,
		"trade_flow": trade_flow,
		"country1": country1,
		"country2": country2,
		"product": product,
		"year": year,
		"trade_flow_list": trade_flow_list,
		"country1_list": country1_list,
		"country2_list": country2_list,
		"product_list": product_list,
		"year1_list": year1_list,
		"year2_list": year2_list,
		"year_interval": year_interval,
		"year_interval_list": year_interval_list})