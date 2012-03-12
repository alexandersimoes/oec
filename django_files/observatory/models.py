from django.db import models
from django.db.models import Sum

###############################################################################
# country tables
###############################################################################
class Country_region(models.Model):
	name = models.CharField(max_length=50, null=True)
	color = models.CharField(max_length=7, null=True)
	text_color = models.CharField(max_length=7, null=True)

	def __unicode__(self):
		return self.name

class Country_manager(models.Manager):
	
	def filter_lang(self, lang):
		return self.extra(select={"name": "name_"+lang})
	
	def get_all(self, lang):
		
		if type(lang) == bool:
			lang = "en"
		lang = lang.replace("-", "_")
		
		countries = self.filter_lang(lang)
		countries = countries.filter(region__isnull=False, name_3char__isnull=False, name_2char__isnull=False).order_by("name_"+lang)
		return list(countries.values(
			"id",
			"name",
			"name_3char",
			"name_2char",
			"region_id",
			"region__color",
			"region__name",
			"region__text_color"
		))

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
	name_ar = models.TextField(null=True)
	name_de = models.TextField(null=True)
	name_el = models.TextField(null=True)
	name_en = models.TextField(null=True)
	name_es = models.TextField(null=True)
	name_fr = models.TextField(null=True)
	name_he = models.TextField(null=True)
	name_hi = models.TextField(null=True)
	name_it = models.TextField(null=True)
	name_ja = models.TextField(null=True)
	name_ko = models.TextField(null=True)
	name_nl = models.TextField(null=True)
	name_ru = models.TextField(null=True)
	name_pt = models.TextField(null=True)
	name_tr = models.TextField(null=True)
	name_zh_cn = models.TextField(null=True)
	
	def __unicode__(self):
		return self.name
	
	def to_json(self):
		return {
			"name": self.name_en,
			"name_3char": self.name_3char}
	
	objects = Country_manager()

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
class Sitc4_manager(models.Manager):
	
	def filter_lang(self, lang):
		if type(lang) is bool:
			lang = "en"
		else:
			lang = lang.replace("-", "_")
		return self.extra(select={"name": "name_"+lang})
	
	def get_all(self, lang):
		
		products = self.filter_lang(lang)
		products = products.filter(community__isnull=False, ps_size__isnull=False)	
		return list(products.values(
			"id",
			"name",
			"code",
			"community_id",
			"community__color",
			"community__name",
			"community__text_color",
			"ps_x",
			"ps_y",
			"ps_size"
		))
		
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
	
	def to_json(self):
		return {
			"name": self.name_en,
			"community_id": self.community.id}
	
	objects = Sitc4_manager()

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
class Sitc4_cpy_manager(models.Manager):
	
	def set_value(self, trade_flow):
		if trade_flow == "net_export":
			return self.extra({'value': 'export_value-import_value'}, where=['export_value-import_value > 0'])
		elif trade_flow == "net_import":
			return self.extra({'value': 'import_value-export_value'}, where=['import_value-export_value > 0'])
		return self.extra(select={"value": "%s_value" % (trade_flow,)})
	
	# def casy(self, country, trade_flow):
	# 	from django.db import connection
	# 	cursor = connection.cursor()
	# 	cursor.execute("""
	# 		SELECT product_id as item_id, year, rca, export_value-import_value as value
	# 		FROM observatory_sitc4_cpy
	# 		WHERE country_id = %d and value > 0""" % country.id)
	# 	result_list = []
	# 	for row in cursor.fetchall():
	# 		raise Exception(row)
	# 		p = self.model(id=row[0], question=row[1], poll_date=row[2])
	# 		p.num_responses = row[3]
	# 		result_list.append(p)
	# 	return result_list

	def casy(self, country, trade_flow):
		
		q_set = self.set_value(trade_flow)
		
		data = q_set.filter(
			country = country,
			product__community__isnull = False,
			product__ps_x__isnull = False).extra(select={'item_id': "product_id"})
			
		return list(data.values("item_id", "year", "value", "rca"))
	
	def sapy(self, product, trade_flow):
		
		q_set = self.set_value(trade_flow)
		
		data = q_set.filter(
			product = product,
			country__region__isnull=False,
			country__name_3char__isnull=False,
			country__name_2char__isnull=False).extra(select={'item_id': "country_id"})

		return list(data.values("item_id", "year", "value", "rca"))

class Sitc4_cpy(models.Model):
	country = models.ForeignKey(Country)
	product = models.ForeignKey(Sitc4)
	year = models.PositiveSmallIntegerField(max_length=4)
	export_value = models.FloatField(null=True)
	import_value = models.FloatField(null=True)
	rca = models.FloatField(null=True)
	
	def __unicode__(self):
		return "CPY: %s.%s.%d" % (self.country.name, self.product.code, self.year)
	
	objects = Sitc4_cpy_manager()

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
class Sitc4_ccpy_manager(models.Manager):

	# if(trade_flow == "export"):
	# 	data = Sitc4_ccpy.objects.filter(origin=c, destination__region__isnull=False, destination__name_3char__isnull=False, destination__name_2char__isnull=False).exclude(destination=231).extra(select={'item_id': "destination_id"})
	# else:
	# 	data = Sitc4_ccpy.objects.filter(destination=c, origin__region__isnull=False, origin__name_3char__isnull=False, origin__name_2char__isnull=False, product__community__isnull=False).exclude(origin=231).extra(select={'item_id': "origin_id"})
	# data = data.values("item_id", "year").annotate(value=Sum('value'))
	
	def csay(self, country1, trade_flow):
		
		if trade_flow == "import":
			data = self.filter(
				destination = country1,
				origin__region__isnull=False,
				origin__name_3char__isnull=False,
				origin__name_2char__isnull=False).extra(select={'item_id': "origin_id"})
			data = data.exclude(origin=231)
		else:
			data = self.filter(
				origin = country1,
				destination__region__isnull=False,
				destination__name_3char__isnull=False,
				destination__name_2char__isnull=False).extra(select={'item_id': "destination_id"})
			
		return list(data.values("item_id", "year").annotate(value=Sum('value')))
	
	def ccsy(self, country1, country2, trade_flow):
		
		if trade_flow == "import":
			country1, country2 = country2, country1
	
		data = self.filter(
			destination = country2,
			origin = country1,
			product__community__isnull = False,
			product__ps_x__isnull = False).extra(select={'item_id': "product_id"})
	
		return list(data.values("item_id", "year", "value"))
	
	def cspy(self, country1, product, trade_flow):
		
		if trade_flow == "import":
			data = self.filter(
				product = product,
				destination = country1,
				origin__region__isnull=False,
				origin__name_3char__isnull=False,
				origin__name_2char__isnull=False).extra(select={'item_id': "origin_id"})
			data = data.exclude(origin=231)
		else:
			data = self.filter(
				product = product,
				origin = country1,
				destination__region__isnull=False,
				destination__name_3char__isnull=False,
				destination__name_2char__isnull=False).extra(select={'item_id': "destination_id"})
			data = data.exclude(destination=231)
	
		return list(data.values("item_id", "year", "value"))
		
		
		# if trade_flow == "export":
		# 	data = Sitc4_ccpy.objects.filter(product=p, origin=c, destination__region__isnull=False, destination__name_3char__isnull=False, destination__name_2char__isnull=False).exclude(destination=231).values("destination_id", "year", "value");
		# elif trade_flow == "import":
		# 	data = Sitc4_ccpy.objects.filter(product=p, destination=c, origin__region__isnull=False, origin__name_3char__isnull=False, origin__name_2char__isnull=False).exclude(origin=231).values("origin_id", "year", "value");
		# 	meta["filter_id"] = "origin_id"
	
class Sitc4_ccpy(models.Model):
	year = models.PositiveSmallIntegerField(max_length=4)
	origin = models.ForeignKey(Country, related_name="sitc4_ccpys_origin")
	destination = models.ForeignKey(Country, related_name="sitc4_ccpys_destination")
	product = models.ForeignKey(Sitc4)
	value = models.FloatField(null=True)

	def __unicode__(self):
		return "%s -> %s" % (self.origin.name, self.destination.name)
	
	objects = Sitc4_ccpy_manager()

class Hs6_ccpy(models.Model):
	year = models.PositiveSmallIntegerField(max_length=4)
	origin = models.ForeignKey(Country, related_name="hs6_ccpys_origin")
	destination = models.ForeignKey(Country, related_name="hs6_ccpys_destination")
	product = models.ForeignKey(Hs6)
	value = models.FloatField(null=True)

	def __unicode__(self):
		return "%s -> %s" % (self.origin.name, self.destination.name)