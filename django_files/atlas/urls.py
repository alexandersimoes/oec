#from django.conf.urls import patterns, include, url
#from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
  (r'^new_ps/', 'observatory.views.new_ps'),
  # internationalization ######################################################
  (r'^i18n/', include('django.conf.urls.i18n')),
  (r'^set_language/(?P<lang>[a-z-]{2,5})/$', 'observatory.views.set_language'),
  
  # product classification ####################################################
  (r'^set_product_classification/(?P<prod_class>[a-z0-9]{3,5})/$', 'observatory.views.set_product_classification'),
  
  # general site ############################################################
  (r'^$', 'observatory.views.home'),
  (r'^download/$', 'observatory.views.download'),
  
  # about section ###########################################################
  (r'^about/$', 'observatory.views.about'),
  (r'^about/team/$', "observatory.views.team"),
  (r'^about/data/$', redirect_to, {'url': '/about/data/sitc4/'}),
  (r'^about/data/(?P<data_type>\w+)/$', "observatory.views.about_data"),
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
  (r'^explore/$', redirect_to, {'url': '/explore/tree_map/export/usa/all/show/2010/'}),
  (r'^explore/(?P<app_name>[a-z_]+)/(?P<trade_flow>\w{6,10})/(?P<country1>\w{3,4})/(?P<country2>\w{3,4})/(?P<product>\w{3,4})/(?P<year>[0-9\.]+)/$', 'observatory.views.explore'),
  (r'^explore/(?P<app_name>[a-z_]+)/(?P<trade_flow>\w{6,10})/(?P<country1>\w{3,4})/(?P<country2>\w{3,4})/(?P<product>\w{3,4})/$', 'observatory.views.explore'),
  
  # Find similar countries
  # (r'^similar/(?P<country>\w{2,3})/(?P<year>[0-9\.]+)/$', 'observatory.views.similar'),
  (r'^similar_wdi/(?P<country>\w{2,3})/(?P<indicator>\d+)/(?P<year>[0-9\.]+)/$', 'observatory.views.similar_wdi'),
    
  # Embed URL
  (r'^embed/(?P<app_name>[a-z_]+)/(?P<trade_flow>\w{6,10})/(?P<country1>\w{3,4})/(?P<country2>\w{3,4})/(?P<product>\w{3,4})/(?P<year>[0-9\.]+)/$', 'observatory.views.embed'),

  # API #######################################################################
  (r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/all/show/(?P<year>[0-9\.]+)/$', 'observatory.views.api_casy'),
  (r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/show/all/(?P<year>[0-9\.]+)/$', 'observatory.views.api_csay'),
  (r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/(?P<country2>\w{3})/show/(?P<year>[0-9\.]+)/$', 'observatory.views.api_ccsy'),
  (r'^api/(?P<trade_flow>[a-z_]{6,10})/(?P<country1>\w{3})/show/(?P<product>\w{4})/(?P<year>[0-9\.]+)/$', 'observatory.views.api_cspy'),
  (r'^api/(?P<trade_flow>[a-z_]{6,10})/show/all/(?P<product>\w{4})/(?P<year>[0-9\.]+)/$', 'observatory.views.api_sapy'),
  
  (r'^api/near/(?P<country>\w{3})/(?P<year>[0-9\.]+)/(?P<num_prods>\d+)/$', 'observatory.views_exhibit.api_near'),
  
  # Overview (Countries) ######################################################
  (r'^country/(?P<country>\w{2,3})/$', 'observatory.views_overview.country2'),
  (r'^hs4/(?P<product>\d{4})/$', 'observatory.views_overview.product'),
  (r'^sitc4/(?P<product>\d{4})/$', 'observatory.views_overview.product'),
  # (r'^profile/(?P<country>\w{2,3})/(?P<trade_flow>[a-z_]{6})/$', 'observatory.views_overview.country'),
  
  # Overview (Products) ######################################################
  (r'^overview/(?P<product>\d{4})/$', 'observatory.views_overview.product'),
  (r'^overview/(?P<product>\d{4})/(?P<trade_flow>[a-z_]{6})/$', 'observatory.views_overview.product'),

  # Rankings ##################################################################
  (r'^rankings/$', 'observatory.views_rankings.index'),
  (r'^rankings/(?P<category>\w{7})/$', 'observatory.views_rankings.index'),
  (r'^rankings/(?P<category>\w{7})/(?P<year>[0-9\.]+)/$', 'observatory.views_rankings.index'),
  (r'^rankings/(?P<category>\w{7})/download/$', 'observatory.views_rankings.download'),
  (r'^rankings/(?P<category>\w{7})/(?P<year>[0-9\.]+)/download/$', 'observatory.views_rankings.download'),
  
  # Exhibit ###################################################################
  (r'^exhibit/$', 'observatory.views_exhibit.index'),
  (r'^exhibit/country_selection/$', 'observatory.views_exhibit.country_selection'),
  (r'^exhibit/product_selection/$', 'observatory.views_exhibit.product_selection'),
  (r'^exhibit/year_selection/$', 'observatory.views_exhibit.year_selection'),
)