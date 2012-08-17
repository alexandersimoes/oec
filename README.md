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

1. Create the folder you'd like The Observatory to live

        mkdir observatory
2. Clone from github

        git clone https://github.com/alexandersimoes/atlas_economic_complexity.git
3. Create the virtual environment

        mkvirtualenv observatory
4. Activate this newly created environment

        workon observatory
5. Install the required Python libraries

        pip install -r requirements.txt
6. Create local settings file based on missing info from settings.py

        touch django_files/atlas/settings_local.py
7. Install MySQL database on local machine using db/observatory_2012-08-17.sql.bz2

