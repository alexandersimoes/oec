# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.translation import gettext as _
from django.utils import translation

supported_langs = [
	('en', 'usa'),
	('es', 'esp'),
	('tr', 'tur'),
	('ja', 'jpn'),
	('it', 'ita'),
	('de', 'deu'),
	('el', 'grc'),
	('fr', 'fra'),
	('he', 'isr'),
	('ar', 'sau'),
	('zh-cn', 'chn'),
	('ru', 'rus'),
	('nl', 'nld'),
	('pt', 'prt'),
	('hi', 'ind'),
	('ko', 'kor'),
]

def set_language(request, lang):
	# output = _("Welcome to my site.")
	# return HttpResponse(output)
	next = request.REQUEST.get('next', None)
	if not next:
		next = request.META.get('HTTP_REFERER', None)
	if not next:
		next = '/'
	response = HttpResponseRedirect(next)
	# if request.method == 'GET':
	# 	lang_code = request.GET.get('language', None)
	lang_code = lang
	if lang_code:
		if hasattr(request, 'session'):
			request.session['django_language'] = lang_code
		else:
			response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
			translation.activate(lang_code)
	return response