import argparse, sys

'''Get command line arguments'''
help_text_year = "the year of data being converted "
help_text_table = "table to perform growth calculations on i.e. ybi, ybio, yb etc "
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help=help_text_year)
parser.add_argument("-t", "--table", help=help_text_table)
parser.add_argument("-d", "--delete", action='store_true', default=False)
args = parser.parse_args()

'''Boolean flag of whether or not to delete previous file, defaults
    to false'''
DELETE_PREVIOUS_FILE = args.delete

'''Need to know year to figure out which folder to use'''
YEAR = args.year
if not YEAR:
    YEAR = raw_input(help_text_year)

TABLE = args.table

print;
print "Year:", YEAR
print;