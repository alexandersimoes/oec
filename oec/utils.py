import sys
from re import sub
from jinja2 import Markup
from flask import abort, current_app, jsonify, request, g, get_flashed_messages, url_for
from datetime import datetime, date, timedelta
from math import ceil
from decimal import *
from sqlalchemy import func, and_, or_, asc, desc, not_

############################################################
# ----------------------------------------------------------
# Utility methods for entire site
# 
############################################################

''' A Mixin class for retrieving public fields from a model
    and serializing them to a json-compatible object'''
class AutoSerialize(object):
    __public__ = None

    def serialize(self):
        
        data = self.__dict__
        allowed = []
        
        for key, value in data.iteritems():
            
            if isinstance(value,Decimal) or \
                isinstance(value,long):
                value = float(value)
            
            if isinstance(value,unicode) or \
                isinstance(value,float) or \
                isinstance(value,int) or \
                isinstance(value,str):
                allowed.append((key,value))

        data = dict(allowed)
        
        return data

''' A helper class for dealing with injecting times into the page using moment.js'''
class Momentjs:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        
    def __call__(self, *args):
        return self.format(*args)

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
        
class formatter:
    def __init__(self, text):
        self.text = text
        
    def __call__(self, *args):
        return self.format(*args)
        
    def render(self, type, lang):
        if isinstance(self.text,unicode) or isinstance(self.text,str):
            format = "text"
        else:
            format = "number"
            
        return Markup("<script>\ndocument.write(dataviva.format.%s(\"%s\",\"%s\",\"%s\"))\n</script>" % (format, self.text, type, str(lang)))

''' A helper funciton for stripping out html tags for showing snippets of user submitted content'''
def strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)

def format_currency(value):
    return "${:,.2f}".format(value)

def format_percent(value):
    return "{:.2g}%".format(value)

def langify(path, lang):
    possible_langs = g.supported_langs.keys()
    url_parts = path.split("/")
    if url_parts[1] in possible_langs:
        url_parts[1] = lang
    else:
        return url_for('general.home', lang=lang)
    return "/".join(url_parts)

''' A helper function for retrieving a specific item from the given model that
    will raise a 404 error if not found in the DB'''
def exist_or_404(Model, id):
    item = Model.query.get(id)
    if item:
        return item
    abort(404, 'Entry not found in %s with id: %s' % (Model.__tablename__, id))

''' Helper function for seeing what SQLAlchemy is actually running on the DB
    http://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression '''
def compile_query(query):
    from sqlalchemy.sql import compiler
    from MySQLdb.converters import conversions, escape

    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = []
    for k in comp.positiontup:
        v = comp.params[k]
        if isinstance(v, unicode):
            v = v.encode(enc)
        params.append( escape(v, conversions) )
    return (comp.string.encode(enc) % tuple(params)).decode(enc)

def make_query(data_table, url_args, lang, join_table=None, classification=None, output_depth=None, **kwargs):
    # from oec.db_attr.models import Country, Hs, Sitc
    from oec.db_attr.models import Country, Hs92, Hs96, Hs02, Hs07
    prod_attr_tbl_lookup = {"hs92":Hs92, "hs96":Hs96, "hs02":Hs02, "hs07":Hs07}
    query = getattr(data_table, "query", None) or data_table
    data_table = join_table or data_table
    ret = {}
    
    '''Go through each of the filters from the URL and apply them to
        the query'''
    for filter in ["year", "origin_id", "dest_id", "hs_id", "sitc_id"]:
        if filter in kwargs:
            
            '''Dealing with year is a special case where we have to check for 
                periods which allow users to select "periods" of data in the 
                format start.end.interval i.e. 2000.2004.2 would return data 
                for the years 2000, 2002, and 2004'''
            if filter == "year":
                if kwargs[filter] != "all":
                    if "." in kwargs[filter]:
                        year_parts = [int(y) for y in kwargs[filter].split(".")]
                        if len(year_parts) == 2:
                            years = range(year_parts[0], year_parts[1]+1)
                        else:
                            years = range(year_parts[0], year_parts[1]+1, year_parts[2])
                    else:
                        years = [kwargs[filter]]
                    query = query.filter(getattr(data_table, filter).in_(years))
            
            elif filter == "origin_id" or filter == "dest_id":
                id = Country.query.filter_by(id_3char=kwargs[filter]).first().id
                query = query.filter(getattr(data_table, filter) == id)
            
            elif filter == "hs_id":
                hs_tbl = prod_attr_tbl_lookup[classification]
                hs_attr_col = getattr(hs_tbl, classification)
                data_tbl_col = getattr(data_table, "{}_id".format(classification))
                id = hs_tbl.query.filter(hs_attr_col == kwargs[filter]).first().id
                query = query.filter(data_tbl_col == id)
            
            elif filter == "sitc_id":
                id = Sitc.query.filter_by(sitc=kwargs[filter]).first().id
                query = query.filter(getattr(data_table, filter) == id)
            
            else:
                query = query.filter(getattr(data_table, filter) == kwargs[filter])
    
    if output_depth:
        col, depth = output_depth.split(".")
        query = query.filter(getattr(data_table, col) == depth)
    
    # raise Exception(compile_query(query))
    if join_table:
        ret["data"] = []
        for tpl in query.all():
            d = {}
            for row in tpl:
                d = dict(d.items() + row.serialize().items())
            ret["data"].append(d)
    else:
        ret["data"] = [row.serialize() for row in query.all()]
    
    '''jsonify result'''
    return jsonify(ret)

def make_cache_key(*args, **kwargs):
    path = request.path
    lang = g.locale
    cache_key = (path + lang).encode('utf-8')
    
    if get_flashed_messages():
        msgs = "|".join([msg[0] for msg in get_flashed_messages(with_categories=True)])
        cache_key += "/"+msgs
    
    return cache_key