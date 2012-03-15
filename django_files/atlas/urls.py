from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
	# internationalization ######################################################
	(r'^i18n/', include('django.conf.urls.i18n')),
	(r'^set_language/(?P<lang>[a-z-]{2,5})/$', 'observatory.views.set_language'),
	
	# general site ############################################################
	(r'^$', 'observatory.views.home'),
	(r'^download/$', 'observatory.views.download'),
	
	# about section ###########################################################
	(r'^about/$', 'observatory.views.about'),
	(r'^about/team/$', "observatory.views.team"),
	(r'^about/team/$', "observatory.views.team"),
	(r'^about/permissions/$', "observatory.views.permissions"),
	# blog
	(r'^about/blog/$', "blog.views.blog_index"),
	url(r'^about/blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', "blog.views.blog_post_detail", name="blog_post"),
	
	# book ###################################################################
	(r'^book/$', 'observatory.views.book'),
	
	# API #######################################################################
	(r'^api/$', 'observatory.views.api'),
	(r'^api/apps/$', 'observatory.views.api_apps'),
	(r'^api/data/$', 'observatory.views.api_data'),
	
	# Explore (App) #############################################################
	# Legacy app redirect
	(r'^app/(?P<app_name>[a-z0-9_]+)/(?P<trade_flow>\w{6,10})/(?P<filter>[a-z0-9\.]+)/(?P<year>[0-9\.]+)/$', 'observatory.views.app_redirect'),
	
	# New app URL structure
	(r'^explore/$', redirect_to, {'url': '/explore/tree_map/export/usa/all/show/2009/'}),
	(r'^explore/(?P<app_name>[a-z_]+)/(?P<trade_flow>\w{6,10})/(?P<country1>\w{3,4})/(?P<country2>\w{3,4})/(?P<product>\w{3,4})/(?P<year>[0-9\.]+)/$', 'observatory.views.explore'),
	
	# Embed URL
	(r'^embed/(?P<app_name>[a-z_]+)/(?P<trade_flow>\w{6,10})/(?P<country1>\w{3,4})/(?P<country2>\w{3,4})/(?P<product>\w{3,4})/(?P<year>[0-9\.]+)/$', 'observatory.views.embed'),

	# API ########################################################################
	(r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/all/show/(?P<year>[0-9\.]+)/$', 'observatory.views.api_casy'),
	(r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/show/all/(?P<year>[0-9\.]+)/$', 'observatory.views.api_csay'),
	(r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/(?P<country2>\w{3})/show/(?P<year>[0-9\.]+)/$', 'observatory.views.api_ccsy'),
	(r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/show/(?P<product>\w{4})/(?P<year>[0-9\.]+)/$', 'observatory.views.api_cspy'),
	(r'^api/(?P<trade_flow>[a-z_]{6,10})/show/all/(?P<product>\w{4})/(?P<year>[0-9\.]+)/$', 'observatory.views.api_sapy'),
)