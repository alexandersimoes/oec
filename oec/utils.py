import cStringIO, gzip, pickle, re, operator, sys
from re import sub
from itertools import groupby
from werkzeug.datastructures import CallbackDict
from jinja2 import Markup
from flask import abort, current_app, make_response, Flask, jsonify, request, Response, session
from functools import update_wrapper
from datetime import datetime, date, timedelta
from math import ceil
from uuid import uuid4
from config import REDIS
from decimal import *
from sqlalchemy import func, and_, or_, asc, desc, not_
from uuid import uuid4

from flask.sessions import SessionInterface, SessionMixin

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
    return "{:.2g} %".format(value)

''' A helper function for retrieving a specific item from the given model that
    will raise a 404 error if not found in the DB'''
def exist_or_404(Model, id):
    item = Model.query.get(id)
    if item:
        return item
    abort(404, 'Entry not found in %s with id: %s' % (Model.__tablename__, id))

''' Helper function to gzip JSON data (used in data API views)'''
def gzip_data(json):
    # GZip all requests for lighter bandwidth footprint
    gzip_buffer = cStringIO.StringIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
    gzip_file.write(json)
    gzip_file.close()
    return gzip_buffer.getvalue()

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None):
    c = current_app.config.get('REDIS_CACHE')
    if c is None:
        return None
    if data is None:
        return c.get(id)
    return c.set(id, data)

''' We are using a custom class for storing sessions on the serverside instead
    of clientside for persistance/security reasons. See the following:
    http://flask.pocoo.org/snippets/75/ '''
class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = REDIS
        if redis is None:
            self.redis = None
            self.prefix = None
        else:
            self.redis = redis
            self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

def make_query(data_table, url_args, lang, **kwargs):
    query = data_table.query
    cache_id = request.path
    ret = {}
    
    cached_q = cached_query(cache_id)
    if cached_q:
        return cached_q
    
    '''Go through each of the filters from the URL and apply them to
        the query'''
    for filter in ["year", "origin_id", "dest_id", "hs_id", "sitc_id"]:
        if filter in kwargs:
            
            '''Dealing with year is a special case where we have to check for 
                periods which allow users to select "periods" of data in the 
                format start.end.interval i.e. 2000.2004.2 would return data 
                for the years 2000, 2002, and 2004'''
            if filter == "year":
                if "." in kwargs[filter]:
                    year_parts = [int(y) for y in kwargs[filter].split(".")]
                    if len(year_parts) == 2:
                        years = range(year_parts[0], year_parts[1]+1)
                    else:
                        years = range(year_parts[0], year_parts[1]+1, year_parts[2])
                else:
                    years = [kwargs[filter]]
                query = query.filter(getattr(data_table, filter).in_(years))
            
            else:
                query = query.filter(getattr(data_table, filter) == kwargs[filter])
    
    ret["data"] = [row.serialize() for row in query.all()]
    
    '''gzip and jsonify result'''
    ret = gzip_data(jsonify(ret).data)
    
    cached_query(cache_id, ret)
    
    return ret