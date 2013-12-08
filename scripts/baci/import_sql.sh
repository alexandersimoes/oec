#!/bin/bash

year_start=$1
year_end=$1
if [ -z "$1" ]; then
  # years={1995..2011}
  year_start=1995
  year_end=2011
fi

tables=($2)
if [ -z "$2" ]; then
  tables=(yd ydp yo yod yodp yop yp)
fi

# for year in ${years[*]}
for (( year=$year_start; year<=$year_end; year++ ))
do
  for table in ${tables[*]}
  do
    
    if [ $table = "yd" ]; then
      file=yd.tsv.bz2
      fields=(year destination_id export_val import_val)
    fi

    if [ $table = "ydp" ]; then
      file=ydp.tsv.bz2
      fields=(year destination_id hs_id export_val import_val)
    fi

    if [ $table = "yo" ]; then
      file=yo.tsv.bz2
      fields=(year origin_id export_val import_val)
    fi

    if [ $table = "yod" ]; then
      file=yod.tsv.bz2
      fields=(year origin_id destination_id export_val import_val)
    fi

    if [ $table = "yodp" ]; then
      file=yodp.tsv.bz2
      fields=(year origin_id destination_id hs_id export_val import_val)
    fi

    if [ $table = "yop" ]; then
      file=yop.tsv.bz2
      fields=(year origin_id hs_id export_val import_val export_rca import_rca)
    fi

    if [ $table = "yp" ]; then
      file=yp.tsv.bz2
      fields=(year hs_id export_val import_val)
    fi
    
    file=$DATA_DIR"/baci/$year/$file"
    sql_fields="("
    sql_set=""
    
    for field in ${fields[*]}
    do
      sql_fields+="@v$field, "
      sql_set+="$field = nullif(@v$field,''), "
    done
    
    sql_set=${sql_set%", "}
    sql_fields=${sql_fields%", "}
    sql_fields+=") "
    
    if [ ! -f $file ]; then
        echo "File not found!"
    fi
    
    bunzip2 -k $file
    file=${file%".bz2"}
    echo $file
    
    if [[ -z $OEC_DB_PW ]]; then
      mysql -u $OEC_DB_USER -e "load data local infile '$file' into table hs_$table fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
    else
      mysql -u $OEC_DB_USER -p $OEC_DB_PW -e "load data local infile '$file' into table hs_$table fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
    fi
    
    rm $file
    
  done
done