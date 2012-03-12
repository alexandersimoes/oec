# -*- coding: utf-8 -*-
from django.db import models

# import urllib2
# 
from datetime import datetime
# 
# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
# from django.db import models
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.utils import simplejson as json
# 
# from django.contrib.sites.models import Site

from django.db.models.query import Q


class PostManager(models.Manager):
    
    def published(self):
        return self.exclude(published=None)
    
    def current(self):
        return self.published().order_by("-published")
    
    def section(self, value, queryset=None):
        
        if queryset is None:
            queryset = self.published()
        
        if not value:
            return queryset
        else:
            try:
                section_idx = self.model.section_idx(value)
            except KeyError:
                raise InvalidSection
            all_sections = Q(section=self.model.section_idx(ALL_SECTION_NAME))
            return queryset.filter(all_sections | Q(section=section_idx))


class Post(models.Model):
	
	title = models.CharField(max_length=90)
	slug = models.SlugField()

	teaser_html = models.TextField(editable=False)
	content_html = models.TextField(editable=False)
    
	created = models.DateTimeField(default=datetime.now, editable=False) # when first revision was created
	updated = models.DateTimeField(null=True, blank=True, editable=False) # when last revision was create (even if not published)
	published = models.DateTimeField(null=True, blank=True, editable=False) # when last published
	
	@staticmethod
	def section_idx(slug):
		"""
		given a slug return the index for it
		"""
		if slug == ALL_SECTION_NAME:
			return 1
		return dict(zip(ig(SECTIONS, 0), range(2, 2 + len(SECTIONS))))[slug]
	
	def rev(self, rev_id):
		return self.revisions.get(pk=rev_id)

	def current(self):
		"the currently visible (latest published) revision"
		return self.revisions.exclude(published=None).order_by("-published")[0]
    
	def latest(self):
		"the latest modified (even if not published) revision"
		try:
			return self.revisions.order_by("-updated")[0]
		except IndexError:
			return None

	class Meta:
		ordering = ("-published",)
		get_latest_by = "published"
    
	objects = PostManager()
    
	def __unicode__(self):
		return self.title
    
	def save(self, **kwargs):
		self.updated_at = datetime.now()
		super(Post, self).save(**kwargs)
    
	def get_absolute_url(self):
		if self.published:
			name = "blog_post"
			kwargs = {
					"year": self.published.strftime("%Y"),
					"month": self.published.strftime("%m"),
					"day": self.published.strftime("%d"),
					"slug": self.slug,
				}
		else:
			name = "blog_post_pk"
			kwargs = {
				"post_pk": self.pk,
			}
		# raise Exception(kwargs)
		return reverse(name, kwargs=kwargs)

	def inc_views(self):
		self.view_count += 1
		self.save()
		self.current().inc_views()