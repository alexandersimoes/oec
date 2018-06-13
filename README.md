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

### Instructions for Adding a New Year of BACI data

#### 1. Download
Download from [here](http://www.cepii.fr/cepii/en/bdd_modele/download.asp?id=1)

#### 2. Run Scripts
Make sure you have any previous years (1 and 5 years for growth) calculated. If not you can run them as so:

```bash
python scripts/baci/format_data.py data/baci/baci92_2010.rar -y 2010 -o data/baci/ -r 92
```

* warning for import to DB you may need to add this to your local `my.cnf`
```bash
[client]
loose-local-infile=1
