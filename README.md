# The Atlas of Economic Complexity Site

The **Atlas** is a site housing **The Observatory**, the master's thesis work
of Alexander Simoes. This **Observatory** is a tool that allows users to quickly
compose a visual narrative about countries and the products they exchange.


### Data

The observatory provides access to bilateral trade data for roughly 200 countries,
50 years and 1000 different products of the SITC4 revision 2 classification. The
source of the data we are using is:

> 1962 - 2000
>
> [The Center for International Data from Robert Feenstra](http://cid.econ.ucdavis.edu/)
>
> 2001 - 2009
>
> [UN COMTRADE](http://comtrade.un.org/)

### Support

**The Observatory** will run in all modern browsers so long as they have
Javascript turned on and have full support for SVG graphics. This includes 
the latest versions of Firefox, Chrome (Chromium), Safari (WebKit), Opera and IE.

Note: Internet Explorer versions 8 and below will not work as they do not have
SVG support built in.

Adding the Observatory to computer via virtualenv

### Getting The Observatory Running Locally via Virtualenv 

1. Clone from github (this will create an atlas_economic_complexity folder in the current directory)

        git clone https://github.com/alexandersimoes/atlas_economic_complexity.git
2. Create the virtual environment

        mkvirtualenv atlas_economic_complexity
3. Activate this newly created environment

        workon atlas_economic_complexity
4. Install the required Python libraries

        pip install -r requirements.txt
5. Create a MySQL database on your local machine
6. Import the latest dump of the database from [atlas.media.mit.edu/media/db/](http://atlas.media.mit.edu/media/db/)

        mysql -u username -p -h localhost DB_NAME < observatory_xxxx-xx-xx.sql
7. Create local settings file based on missing info from settings.py

        touch django_files/atlas/settings_local.py
8. Edit this file and add the following setting CONSTANTS to it based on comments in django_files/atlas/settings.py

        DATABASES
        LOCALE_PATHS
        STATICFILES_DIRS
        SECRET_KEY
        TEMPLATE_DIRS
        REDIS
        CACHE
				
9. Run the site locally!

        django_files/manage.py runserver_

### Getting The Observatory Running With Redis Caching enabled (Optional)
    
10. If you would like to run the Observatory with a cache (if, for instance, you wished to deploy it on a live server)
    All you will need to do is install the proper libraries and resources --

11. Download, extract and compile Redis itself with:
		
        $ wget http://redis.googlecode.com/files/redis-2.6.7.tar.gz
        $ tar xzf redis-2.6.7.tar.gz
        $ cd redis-2.6.7
        $ make  

12.	Install the redis-py client with (from https://github.com/andymccurdy/redis-py)

        $ sudo easy_install redis
        $ sudo python setup.py install
					
13. Install the django-redis backend (from https://github.com/niwibe/django-redis)
          
        easy_install django_redis
					
14. You will also need the following serialization library: (from http://msgpack.org)									
          
        easy_install msgpack-python
					
15. The constants defined in settings.py have REDIS turned on by default. The example constants in the comments can be used to turn it off. 		 