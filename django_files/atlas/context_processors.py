def media_url(request):
	# from django.conf import settings
	# return {'media_url': settings.MEDIA_URL}
	# return {'media_url': 44}
	return {'ip_address': request.META['REMOTE_ADDR']}

def supported_langs(request):
	from django.utils.translation import get_language_info
	supported_langs = (
		(get_language_info('en'), 'usa'),
		(get_language_info('es'), 'esp'),
		(get_language_info('tr'), 'tur'),
		(get_language_info('ja'), 'jpn'),
		(get_language_info('it'), 'ita'),
		(get_language_info('de'), 'deu'),
		(get_language_info('el'), 'grc'),
		(get_language_info('fr'), 'fra'),
		(get_language_info('he'), 'isr'),
		(get_language_info('ar'), 'sau'),
		(get_language_info('zh-cn'), 'chn'),
		(get_language_info('ru'), 'rus'),
		(get_language_info('nl'), 'nld'),
		(get_language_info('pt'), 'prt'),
		(get_language_info('hi'), 'ind'),
		(get_language_info('ko'), 'kor'),
	)
	return {'supported_langs': supported_langs}