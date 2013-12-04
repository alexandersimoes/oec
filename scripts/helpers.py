# -*- coding: utf-8 -*-
"""
    Helpers
    ~~~~~~~
    
"""

''' Import statements '''
import sys, bz2, gzip, zipfile
from decimal import Decimal, ROUND_HALF_UP
from os.path import splitext, basename, exists

def d(x):
  return Decimal(x).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

def get_file(file_path):
    file_name = basename(file_path)
    file_path, file_ext = splitext(file_path)
    extensions = [
        {'ext': file_ext+'.bz2', 'io':bz2.BZ2File},
        {'ext': file_ext+'.gz', 'io':gzip.open},
        {'ext': file_ext+'.zip', 'io':zipfile.ZipFile},
        {'ext': file_ext, 'io':open}
    ]
    for e in extensions:
        file_path_w_ext = file_path + e["ext"]
        if exists(file_path_w_ext):
            file = e["io"](file_path_w_ext)
            if '.zip' in e["ext"]:
                file = zipfile.ZipFile.open(file, file_name)
            print "Reading from file", file_path_w_ext
            return file
    print "ERROR: unable to find file named {0}[.zip, .bz2, .gz] " \
            "in directory specified.".format(file_name)
    return None

def format_runtime(x):
    # convert to hours, minutes, seconds
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    if h:
        return "{0} hours and {1} minutes".format(int(h), int(m))
    if m:
        return "{0} minutes and {1} seconds".format(int(m), int(s))
    if s < 1:
        return "< 1 second"
    return "{0} seconds".format(int(s))
        