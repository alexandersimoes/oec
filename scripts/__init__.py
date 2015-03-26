# import argparse, sys
# 
# '''Get command line arguments'''
# help_text_year = "the year of data being converted: "
# help_text_table = "table to perform growth calculations on i.e. ybi, ybio, yb etc: "
# help_text_class = "hs or sitc: "
# help_text_file = "full path to file: "
# help_text_lang = "language: "
# 
# parser = argparse.ArgumentParser()
# parser.add_argument("-y", "--year", help=help_text_year)
# parser.add_argument("-f", "--file", help=help_text_file)
# parser.add_argument("-t", "--table", help=help_text_table)
# parser.add_argument("-l", "--lang", help=help_text_lang)
# parser.add_argument("-c", "--classification", help=help_text_class, default=None)
# parser.add_argument("-d", "--delete", action='store_true', default=False)
# args = parser.parse_args()
# 
# '''Boolean flag of whether or not to delete previous file, defaults
#     to false'''
# DELETE_PREVIOUS_FILE = args.delete
# 
# '''Need to know year to figure out which folder to use'''
# YEAR = args.year
# TABLE = args.table
# CLASSIFICATION = args.classification
# FILE = args.file
# LANG = args.lang
# 
# for arg in [YEAR, TABLE, CLASSIFICATION, FILE, LANG]:
#     if arg:
#         print; print arg; print;