# -*- coding: utf-8 -*-
"""
    Import a Directory to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Example Usage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    python db_importer.py --dir=data/baci/2012/ --name=hedu

"""

import click
import os, sys, fnmatch
import re

pattern = re.compile('(\w+).tsv(.bz2)*')


def parse_table(t, dbname):
    m = pattern.search(t)
    if m:
        return dbname + "_" + m.group(1)

# via http://stackoverflow.com/questions/13299731/python-need-to-loop-through-directories-looking-for-txt-files
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

@click.command()
@click.option('-d', '--dir', default='.', type=click.Path(exists=True), prompt=False, help='Directory for tsv files.')
@click.option('-a', '--attr_type', help='Attribute Type', type=click.Choice(['hs', 'sitc']), default='hs')
@click.option('-r', '--revision', help='Product Classification Revision', type=click.Choice(['92', '96', '02', '07']), default=None)
def main(dir, attr_type, revision):
    attr_revision = "{}{}".format(attr_type, revision) if revision else attr_type
    
    for f in findFiles(dir, '{}*.tsv*'.format(attr_revision)):
        bzipped = False
        
        print f, "Processing"
        if f.endswith("bz2"):
            bzipped = True
            os.system("bunzip2 -k " + f)
            f = f[:-4]
        
        handle = open(f)
        
        m = pattern.search(f)
        if m:
            tbl = m.group(1)
            if "attr" in tbl:
                tbl = tbl.replace('hs{}_'.format(revision), '').replace('sitc_', '')
                if bzipped: os.remove(f)
                continue
            # return dbname + "_" + m.group(1)
        
        
        # tablename = parse_table(f, name)
        print "table name =", tbl
        header = handle.readline().strip()
        fields = header.split('\t')
            
        fields = [x for x in fields]

        fields = ",".join(fields)

        cmd = '''mysql -uroot $OEC_DB_NAME -e "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES ({});" '''.format(f, tbl, fields)
        # print cmd
        os.system(cmd)

        # delete bunzipped file
        if bzipped:
            os.remove(f)


if __name__ == '__main__':
    main()