#!/bin/bash

year_start=$1
year_end=$1
if [ -z "$1" ]; then
  year_start=2000
  year_end=2012
fi

tables=($2)
if [ -z "$2" ]; then
  tables=(yd ydp yo yod yodp yop yp)
fi

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
      fields=(year destination_id sitc_id export_val import_val)
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
      fields=(year origin_id destination_id sitc_id export_val import_val)
    fi

    if [ $table = "yop" ]; then
      file=yop.tsv.bz2
      fields=(year origin_id sitc_id export_val import_val export_rca import_rca)
    fi

    if [ $table = "yp" ]; then
      file=yp.tsv.bz2
      fields=(year sitc_id export_val import_val)
    fi
    
    file=$DATA_DIR"/comtrade/$year/$file"
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
      mysql -u $OEC_DB_USER -e "load data local infile '$file' into table sitc_$table fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
    else
      mysql -u $OEC_DB_USER -p $OEC_DB_PW -e "load data local infile '$file' into table sitc_$table fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
    fi
    
    rm $file
    
  done
done
































# years=($1)
# if [ -z "$1" ]; then
#   years={1979..2012}
# fi
# 
# tables=($2)
# if [ -z "$2" ]; then
#   tables=(yd ydp yo yod yodp yop yp)
# fi
# 
# for year in ${years[*]}
# do
#   for table in ${tables[*]}
#   do
#     
#     if [ $2 = "yd" ]; then
#       file=yd.tsv.bz2
#       fields=(year destination_id export_val import_val)
#     fi
# 
#     if [ $2 = "ydp" ]; then
#       file=ydp.tsv.bz2
#       fields=(year destination_id sitc_id export_val import_val)
#     fi
# 
#     if [ $2 = "yo" ]; then
#       file=yo.tsv.bz2
#       fields=(year origin_id export_val import_val)
#     fi
# 
#     if [ $2 = "yod" ]; then
#       file=yod.tsv.bz2
#       fields=(year origin_id destination_id export_val import_val)
#     fi
# 
#     if [ $2 = "yodp" ]; then
#       file=yodp.tsv.bz2
#       fields=(year origin_id destination_id sitc_id export_val import_val)
#     fi
# 
#     if [ $2 = "yop" ]; then
#       file=yop.tsv.bz2
#       fields=(year origin_id sitc_id export_val import_val export_rca import_rca)
#     fi
# 
#     if [ $2 = "yp" ]; then
#       file=yp.tsv.bz2
#       fields=(year sitc_id export_val import_val)
#     fi
#     
#     file=$DATA_DIR"/comtrade/$1/$file"
#     sql_fields="("
#     sql_set=""
# 
#     for field in ${fields[*]}
#     do
#       sql_fields+="@v$field, "
#       sql_set+="$field = nullif(@v$field,''), "
#     done
# 
#     sql_set=${sql_set%", "}
#     sql_fields=${sql_fields%", "}
#     sql_fields+=") "
# 
#     if [ ! -f $file ]; then
#         echo "File not found!"
#     fi
# 
#     bunzip2 -k $file
#     file=${file%".bz2"}
#     echo $file
# 
#     if [[ -z $OEC_DB_PW ]]; then
#       mysql -u $OEC_DB_USER -e "load data local infile '$file' into table sitc_$2 fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
#     else
#       mysql -u $OEC_DB_USER -p $OEC_DB_PW -e "load data local infile '$file' into table sitc_$2 fields terminated by '\t' lines terminated by '\n' IGNORE 1 LINES $sql_fields SET $sql_set" oec --local-infile=1
#     fi
# 
#     rm $file
#     
#   done
# done