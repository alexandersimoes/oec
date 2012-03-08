from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# general site ############################################################
	(r'^$', 'observatory.views.home'),
	
	(r'^about/$', 'observatory.views.about'),
	(r'^about/blog/$', "blog.views.blog_index"),
	(r'^about/team/$', "observatory.views.team"),
	
	(r'^book/$', 'observatory.views.book'),
	
	(r'^api/$', 'observatory.views.api'),
        (r'^api/apps$', 'observatory.views.api_apps'),
        (r'^api/data$', 'observatory.views.api_data'),


)
