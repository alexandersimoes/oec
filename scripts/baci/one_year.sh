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
if [ -z "$3" ]; then
  echo "No third argument supplied, need HS revision [92, 96, 02, 07]"
  exit 1
fi

PWD=/${PWD#*/}

for i in $(seq $1 $2); do 
  echo $i; 

  python scripts/baci/format_data.py \
    $PWD/data/baci/baci$3_$i.rar \
    -y $i \
    -o $PWD/data/baci/ \
    -r $3

  if [ $i -gt "1995" ]; then
    PREV_YEAR=`expr $i - 1`
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yd.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yd.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_ydp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_ydp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yo.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yo.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yod.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yod.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yodp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yodp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yop.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yop.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
  fi

  if [ $i -gt "1999" ]; then
    echo "FIVE YEAR GROWTH for $i"
    PREV_YEAR_FIVE=`expr $i - 5`
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yd.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yd.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_ydp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_ydp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yo.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yo.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yod.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yod.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yodp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yodp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yop.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yop.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id
  fi
  
  echo "Importing..."
  python scripts/common/db_importer.py --dir=$PWD/data/baci/$i/ --attr_type=hs --revision=$3
done