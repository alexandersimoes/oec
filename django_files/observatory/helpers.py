from observatory.models import *

# make sure app name is in the list of possible apps
def get_app_name(app_name):
  possible_apps = ["tree_map", "stacked", "product_space", "map"]
  
  # if the app_name requested is not in the list of possibilities
  if app_name not in possible_apps:
    app_name = None
  
  return app_name


# make sure this is accepted trade_flow
def get_trade_flow(trade_flow):
  possible_yoga_flows = ["export", "import", "net_export", "net_import"]
  
  if trade_flow not in possible_yoga_flows:
    trade_flow = None
  
  return trade_flow  


def get_years(classification):
  # get distince years from db, different for diff product classifications
  
  if classification == "sitc4":
    years_available = list(Sitc4_cpy.objects.values_list("year", flat=True).distinct())
  elif classification == "hs4":
    years_available = list(Hs4_cpy.objects.values_list("year", flat=True).distinct())
  
  return years_available


# Returns app type in CCPY format  
def get_app_type(country1, country2, product, year):
  
  # country / all / show / year
  if country2 == "all" and product == "show":
    return "casy"
  
  # country / show / all / year
  elif country2 == "show" and product == "all":
    return "csay"
  
  # show / all / product / year
  elif country1 == "show" and country2 == "all":
    return "sapy"
  
  # country / country / show / year
  elif product == "show":
    return "ccsy"
  
  #  country / show / product / year
  else:
    return "cspy"


# Returns the Country object or None
def get_country(country):
  # first try looking up based on 3 character code
  try:
    c = Country.objects.get(name_3char=country)
  except Country.DoesNotExist:
    # next try 2 character code
    try:
      c = Country.objects.get(name_2char=country)
    except Country.DoesNotExist:
      c = None
  return c


# Returns the Product object or None
def get_product(product, classification):
  # first try looking up based on 3 character code
  if classification == "hs4":
    try:
      p = Hs4.objects.get(code=product)
    except Hs4.DoesNotExist:
      # next try SITC4
      try:
        conv_code = Sitc4.objects.get(code=product).conversion_code
        p = Hs4.objects.get(code=conv_code)
      except Sitc4.DoesNotExist:
        p = None
  else:
    try:
      p = Sitc4.objects.get(code=product)
    except Sitc4.DoesNotExist:
      # next try SITC4
      try:
        conv_code = Hs4.objects.get(code=product).conversion_code
        p = Sitc4.objects.get(code=conv_code)
      except Hs4.DoesNotExist:
        p = None
  return p


# Returns the question to display on the page describing the URL requested
def get_question(app_type, **kwargs):
  
  trade_flow = kwargs["trade_flow"]
  
  if app_type == "casy":
    origin = kwargs["origin"] 
    
    if trade_flow in ['net_export','net_import']:
      title =  "What does %s %s in net terms?" % (origin.name, trade_flow.replace("_", " ").split()[1])
    else:
      title = "What does %s %s?" % (origin.name, trade_flow.replace("_", " "))
  
  # Country but showing other country trade partners
  elif app_type == "csay":
    origin = kwargs["origin"] 
    
    article = "to" if trade_flow in ["export","net_export"] else "from"
    if trade_flow in ['net_export','net_import']:
      title = "Where does %s %s %s in net terms? " % (origin.name, trade_flow.replace("_", " ").split()[1], article) 
    else:
      title = "Where does %s %s %s?" % (origin.name, trade_flow.replace("_", " "), article)  
  
  # Product
  elif app_type == "sapy":
    product = kwargs["product"]
      
    if trade_flow in ['net_export','net_import']:
      title = "Who %ss %s in net terms?" % (trade_flow.replace("_", " ").split()[1], product.name_en) 
    else: 
      title = "Who %ss %s?" % (trade_flow.replace("_", " "), product.name_en)
    
  # Bilateral Country x Country
  elif app_type == "ccsy":
    origin = kwargs["origin"]
    destination = kwargs["destination"]
    
    article = "to" if trade_flow in ["export","net_export"] else "from"
    if trade_flow in ['net_export','net_import']:
      title = "What does %s %s %s %s in net terms?" % (origin.name, trade_flow.replace("_", " ").split()[1], article, destination.name)
    else:
      title = "What does %s %s %s %s?" % (origin.name, trade_flow, article, destination.name)
  
  # Bilateral Country / Show / Product / Year
  elif app_type == "cspy":
    origin = kwargs["origin"] 
    product = kwargs["product"]
    
    article = "to" if trade_flow in ["export","net_export"] else "from"
    if trade_flow in ['net_export','net_import']:
      title = "Where does %s %s %s %s in net terms?" % (origin.name, trade_flow.replace("_", " ").split()[1], product.name_en, article)
    else:
      title = "Where does %s %s %s %s?" % (origin.name, trade_flow, product.name_en, article)
  
  return title
