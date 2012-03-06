from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
	# general site ############################################################
	(r'^$', 'observatory.views.home'),
	# about section
	(r'^about/$', 'observatory.views.about'),
	(r'^about/blog/$', "blog.views.blog_index"),
	(r'^about/team/$', "observatory.views.team"),
	# book
	(r'^book/$', 'observatory.views.book'),
	# api
	# (r'^api/$', 'observatory.views.api'),
	(r'^api/$', redirect_to, {'url': 'http://web.media.mit.edu/~simoes/embed/'}),
	
	# app #####################################################################
	(r'^app/(?P<app_name>[a-z0-9_]+)/(?P<trade_flow>\w{6,10})/(?P<filter>[a-z0-9\.]+)/(?P<year>[0-9\.]+)/$', 'observatory.views.app'),
)
