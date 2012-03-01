from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # general site ############################################################
		(r'^$', 'observatory.views.home'),
)
