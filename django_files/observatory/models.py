from django.db import models

###############################################################################
# country tables
###############################################################################
class Country_region(models.Model):
	name = models.CharField(max_length=50, null=True)
	color = models.CharField(max_length=7, null=True)
	text_color = models.CharField(max_length=7, null=True)

	def __unicode__(self):
		return self.name

class Country(models.Model):
	name = models.CharField(max_length=200)
	name_numeric = models.PositiveSmallIntegerField(max_length=4, null=True)
	name_2char = models.CharField(max_length=2, null=True)
	name_3char = models.CharField(max_length=3, null=True)
	continent = models.CharField(max_length=50, null=True)
	region = models.ForeignKey(Country_region, null=True)
	capital_city = models.CharField(max_length=100, null=True)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	coordinates = models.TextField(null=True)
	
	def __unicode__(self):
		return self.name

###############################################################################
# product tables
###############################################################################
# Colors for leamer classification of products
class Sitc4_leamer(models.Model):
	name = models.CharField(max_length=30)
	color = models.CharField(max_length=7)
	img = models.FilePathField(null=True)

	def __unicode__(self):
		return self.name + " color: " + self.color

# Colors for Michele Coscia community clustering algorithm
class Sitc4_community(models.Model):
	code = models.CharField(max_length=4)
	name = models.CharField(max_length=100, null=True)
	color = models.CharField(max_length=7, null=True)
	text_color = models.CharField(max_length=7, null=True)
	img = models.FilePathField(null=True)

	def __unicode__(self):
		return self.code

# SITC4 products
class Sitc4(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=4)
	leamer = models.ForeignKey(Sitc4_leamer, null=True)
	community = models.ForeignKey(Sitc4_community, null=True)
	ps_x = models.FloatField(null=True)
	ps_y = models.FloatField(null=True)
	ps_size = models.FloatField(null=True)
	ps_x_classic = models.FloatField(null=True)
	ps_y_classic = models.FloatField(null=True)
	ps_size_classic = models.FloatField(null=True)
	name_ar = models.TextField(null=True) # Arabic
	name_de = models.TextField(null=True) # German
	name_el = models.TextField(null=True) # Greek
	name_en = models.TextField(null=True) # English
	name_es = models.TextField(null=True) # Spanish
	name_fr = models.TextField(null=True) # France
	name_he = models.TextField(null=True) # Hebrew
	name_hi = models.TextField(null=True) # Hindi
	name_it = models.TextField(null=True) # Italy
	name_ja = models.TextField(null=True) # Japanese
	name_ko = models.TextField(null=True) # Korean
	name_nl = models.TextField(null=True) # Dutch
	name_ru = models.TextField(null=True) # Russian
	name_pt = models.TextField(null=True) # Portuguese
	name_tr = models.TextField(null=True) # Turkish
	name_zh_cn = models.TextField(null=True) # Simplified Chinese

	def __unicode__(self):
		return self.code + self.name_en

# HS6 Products
class Hs6(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=4)
	ps_x = models.FloatField(null=True)
	ps_y = models.FloatField(null=True)
	ps_size = models.FloatField(null=True)
	name_ar = models.TextField(null=True) # Arabic
	name_de = models.TextField(null=True) # German
	name_el = models.TextField(null=True) # Greek
	name_en = models.TextField(null=True) # English
	name_es = models.TextField(null=True) # Spanish
	name_fr = models.TextField(null=True) # France
	name_he = models.TextField(null=True) # Hebrew
	name_hi = models.TextField(null=True) # Hindi
	name_it = models.TextField(null=True) # Italy
	name_ja = models.TextField(null=True) # Japanese
	name_ko = models.TextField(null=True) # Korean
	name_nl = models.TextField(null=True) # Dutch
	name_ru = models.TextField(null=True) # Russian
	name_pt = models.TextField(null=True) # Portuguese
	name_tr = models.TextField(null=True) # Turkish
	name_zh_cn = models.TextField(null=True) # Simplified Chinese

	def __unicode__(self):
		return self.code + self.name

###############################################################################
# country - product - year tables
###############################################################################
class Sitc4_cpy(models.Model):
	country = models.ForeignKey(Country)
	product = models.ForeignKey(Sitc4)
	year = models.PositiveSmallIntegerField(max_length=4)
	export_value = models.FloatField(null=True)
	import_value = models.FloatField(null=True)
	rca = models.FloatField(null=True)
	
	def __unicode__(self):
		return "CPY: %s.%s.%d" % (self.country.name, self.prdocut.code, self.year)

class Hs6_cpy(models.Model):
	country = models.ForeignKey(Country)
	product = models.ForeignKey(Hs6)
	year = models.PositiveSmallIntegerField(max_length=4)
	export_value = models.FloatField(null=True)
	import_value = models.FloatField(null=True)
	rca = models.FloatField(null=True)
	
	def __unicode__(self):
		return "CPY: %s.%s.%d" % (self.country.name, self.prdocut.code, self.year)

###############################################################################
# country - country - product - year tables
###############################################################################
class Sitc4_ccpy(models.Model):
	year = models.PositiveSmallIntegerField(max_length=4)
	origin = models.ForeignKey(Country, related_name="sitc4_ccpys_origin")
	destination = models.ForeignKey(Country, related_name="sitc4_ccpys_destination")
	product = models.ForeignKey(Sitc4)
	value = models.FloatField(null=True)

	def __unicode__(self):
		return "%s -> %s" % (self.origin.name, self.destination.name)

class Hs6_ccpy(models.Model):
	year = models.PositiveSmallIntegerField(max_length=4)
	origin = models.ForeignKey(Country, related_name="hs6_ccpys_origin")
	destination = models.ForeignKey(Country, related_name="hs6_ccpys_destination")
	product = models.ForeignKey(Hs6)
	value = models.FloatField(null=True)

	def __unicode__(self):
		return "%s -> %s" % (self.origin.name, self.destination.name)