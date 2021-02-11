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

1. Clone from github (this will create an `oec` folder in the current directory)

        git clone https://github.com/alexandersimoes/oec.git
2. Create the virtual environment

        virtualenv oec
3. Activate this newly created environment

        . /path/to/oec/bin/activate
4. Install required software

        mysql
        # if using homebrew, not install ONLY the client
        brew install mysql --client-only --universal
5. Install the required Python libraries

        pip install -r requirements.txt
6. Create a MySQL database on your local machine
7. Import the latest dump of the database from [18.85.28.32/static/db/](http://18.85.28.32/static/db/) (warning this step could take hours!)

        mysql -u username -p -h localhost DB_NAME < oec_xxxx-xx-xx.sql
8. Be sure to create the following local environment variables

        export OEC_SECRET_KEY=some_s3cret_k3y
        export OEC_DB_USER=my_db_username
        export OEC_DB_PW=my_db_password
        export OEC_DB_HOST=localhost
        export OEC_DB_NAME=oec
        * export CACHE_DIR=/home/

        * only necessary if using filesystem caching
9. Updating translations (if something is changed)

        pybabel extract -F babel.cfg -o messages.pot oec --no-location --omit-header --no-wrap
        pybabel update -i messages.pot -d oec/translations --no-wrap --no-fuzzy-matching -l [2-LETTER-LANG-CODE]
        pybabel compile -d oec/translations -l [2-LETTER-LANG-CODE] --statistics
10. Running the testing server
        
        python run.py runserver


# Deploying to a linux server
### Step 1: Install virtual environments and pip
```$ sudo apt-get install python-virtualenv python-pip git libmysqlclient-dev python-dev```

### Step 2: Create virtual environment
```$ virtualenv oec```
```$ source oec/bin/activate```

### Step 3: Pull in app from github
```$ git clone https://github.com/alexandersimoes/oec.git -b v3.0 —-single-branch```

### Step 4: Install python requirements
```$ pip install -r requirements.txt```

### Step 5: Install gunicorn
```$ pip install gunicorn```

### Step 6: Set environment vars
```
export OEC_SECRET_KEY=yet_another_supers3cret_k35y
export OEC_DB_USER=oec_user
export OEC_DB_PW=oec_pw
export OEC_DB_HOST=localhost
export OEC_DB_NAME=oec
export CACHE_DIR=/home/macro/sites/oec/cache
export OEC_PRODUCTION=1
```

### Step 7: Make cache directory
```$ mkdir /home/macro/sites/oec/cache```

### Step 8: Create nginx config 
```$ sudo nano /etc/nginx/sites-available/oec.conf```

```
server {
    listen 80;
    server_name 104.239.233.5;
 
    root /home/macro/sites/oec;
 
    access_log /home/macro/sites/oec/logs/access.log;
    error_log /home/macro/sites/oec/logs/error.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }
}
```
```$ sudo ln -s /etc/nginx/sites-available/oec.conf /etc/nginx/sites-enabled/```
 
### Step 9: Create dir for logs
```$ mkdir /home/macro/sites/oec/logs```

### Step 10: Check nginx config
```$ sudo nginx -t```

### Step 11: Using supervisor to autostart/manage gunicorn process
```sudo apt-get install supervisor```

### Step 11: Create supervisor config
```$ sudo nano /etc/supervisor/conf.d/oec.conf```

```
[program:oec]
command = /home/macro/venv/oec/bin/gunicorn oec:app
directory = /home/macro/sites/oec
user = macro
stdout_logfile = /home/macro/sites/oec/logs/gunicorn.log
redirect_stderr = true
environment=PATH="/home/macro/venv/oec/bin", OEC_SECRET_KEY="oec-secret-key", OEC_DB_USER="oec_user", OEC_DB_PW="oec_pw", OEC_DB_HOST="localhost", OEC_DB_NAME="oec", CACHE_DIR="/home/macro/sites/oec/cache", OEC_PRODUCTION="1"
```

### Step 12: Start up supervisor
```
$ sudo supervisorctl reread
$ sudo supervisorctl update
$ sudo supervisorctl status oec
```
