#!/bin/bash
set -e # exit script if any commands fail

if [ $# -eq 0 ]; then
  echo "No arguments provided, need a year"
  exit 1
fi

if [ -z "$2" ]; then
  echo "No second argument supplied, ending year"
  exit 1
fi

ONE_YR_GROWTH=1962
FIVE_YR_GROWTH=$ONE_YR_GROWTH
let "FIVE_YR_GROWTH += 5"

PWD=/${PWD#*/}

for i in $(seq $1 $2); do 
  echo $i;
  
  python scripts/comtrade/format_data.py \
    $PWD/data/comtrade_sitc/comtrade_$i.csv \
    -y $i \
    -o $PWD/data/comtrade_sitc/

  if [[ $i -gt $ONE_YR_GROWTH ]]; then
    PREV_YEAR=`expr $i - 1`
    echo "one year growth!"
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yd.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yd.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i 
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_ydp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_ydp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yo.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yo.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s top_export,top_import
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yod.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yod.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yodp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yodp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yop.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yop.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR/sitc_yp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
  fi

  if [ $i -gt $FIVE_YR_GROWTH ]; then
    echo "FIVE YEAR GROWTH for $i"
    PREV_YEAR_FIVE=`expr $i - 5`
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yd.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yd.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_ydp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_ydp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yo.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yo.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s top_export,top_import
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yod.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yod.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yodp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yodp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yop.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yop.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/comtrade_sitc/$i/sitc_yp.tsv.bz2 $PWD/data/comtrade_sitc/$PREV_YEAR_FIVE/sitc_yp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/comtrade_sitc/$i -s sitc_id
  fi
  
  echo "Importing..."
  python scripts/common/db_importer.py --dir=$PWD/data/comtrade_sitc/$i/ --attr_type=sitc
done