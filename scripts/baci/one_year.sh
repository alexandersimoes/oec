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

if [[ $3 == "92" ]]; then
  ONE_YR_GROWTH=1995
fi
if [[ $3 == "96" ]]; then
  ONE_YR_GROWTH=1998
fi
if [[ $3 == "02" ]]; then
  ONE_YR_GROWTH=2003
fi
if [[ $3 == "07" ]]; then
  ONE_YR_GROWTH=2008
fi
FIVE_YR_GROWTH=$ONE_YR_GROWTH
let "FIVE_YR_GROWTH += 5"

PWD=/${PWD#*/}

for i in $(seq $1 $2); do 
  echo $i; 

  python scripts/baci/format_data.py \
    $PWD/data/baci/baci$3_$i.rar \
    -y $i \
    -o $PWD/data/baci/ \
    -r $3

  if [[ $i -gt $ONE_YR_GROWTH ]]; then
    PREV_YEAR=`expr $i - 1`
    echo "one year growth!"
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yd.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yd.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_ydp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_ydp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yo.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yo.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3 -s top_export,top_import
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yod.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yod.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yodp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yodp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yop.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yop.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yp.tsv.bz2 --years=1 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    echo "PCI rank delta!"
    python scripts/baci/rank_delta.py $PWD/data/baci/$i/hs$3_yp.tsv.bz2 $PWD/data/baci/$PREV_YEAR/hs$3_yp.tsv.bz2 --rank_col=pci_rank --index_cols=hs$3_id --strcasts=hs$3_id -o $PWD/data/baci/$i
  fi

  if [ $i -gt $FIVE_YR_GROWTH ]; then
    echo "FIVE YEAR GROWTH for $i"
    PREV_YEAR_FIVE=`expr $i - 5`
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yd.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yd.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_ydp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_ydp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yo.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yo.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3 -s top_export,top_import
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yod.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yod.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yodp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yodp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yop.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yop.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
    python $PWD/scripts/common/growth_calc.py $PWD/data/baci/$i/hs$3_yp.tsv.bz2 $PWD/data/baci/$PREV_YEAR_FIVE/hs$3_yp.tsv.bz2 --years=5 --cols=export_val,import_val -o $PWD/data/baci/$i -s hs$3_id -r $3
  fi
  
  echo "Importing..."
  python scripts/common/db_importer.py --dir=$PWD/data/baci/$i/ --attr_type=hs --revision=$3
done