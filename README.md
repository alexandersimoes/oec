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

1. Clone from github (this will create an oec folder in the current directory)

        git clone https://github.com/alexandersimoes/oec.git
2. Create the virtual environment

        mkvirtualenv oec
3. Activate this newly created environment

        workon oec
4. Install the required Python libraries

        pip install -r requirements.txt
5. Create a MySQL database on your local machine
6. Import the latest dump of the database from [atlas.media.mit.edu/static/db/](http://atlas.media.mit.edu/static/db/)

        mysql -u username -p -h localhost DB_NAME < oec_xxxx-xx-xx.sql
7. Be sure to create the following local environment variables

        export OEC_SECRET_KEY=some_s3cret_k3y
        export OEC_DB_USER=my_db_username
        export OEC_DB_PW=my_db_password
        export OEC_DB_HOST=localhost
        export OEC_DB_NAME=oec
        * export CACHE_DIR=/home/

        * only necessary if using filesystem caching
8. Updating translations (if something is changed)

        pybabel extract -F babel.cfg -o messages.pot oec
        pybabel update -i messages.pot -d oec/translations
        pybabel compile -d oec/translations

