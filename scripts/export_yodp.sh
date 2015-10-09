if [ -z "$1" ]; then
  echo "What dataset?"
  exit 1
fi

end_year=2013
depths=(4 6)
prod_id=$1
if [[ $1 == "hs92" ]]; then
  start_year=1995
fi
if [[ $1 == "hs96" ]]; then
  start_year=1998
fi
if [[ $1 == "hs02" ]]; then
  start_year=2003
fi
if [[ $1 == "hs07" ]]; then
  start_year=2008
  end_year=2012
fi
if [[ $1 == "sitc" ]]; then
  start_year=1962
  file_suffix=sitc_rev2
  prod_id=sitc_rev2
  depths=(false)
fi

echo start year = $start_year
echo end year = $end_year 
echo

for ((i=$start_year;i<=$end_year;i++))
do
  echo year = $i
  for depth in ${depths[*]}
  do
    xtra_mysql=''
    if [ ! "$depth" = false ] ; then
      file_suffix=$1_$depth
      id_len=$depth
      let "id_len += 2"
      xtra_mysql="and $1_id_len = $id_len"
    fi
    
    if [ $i = $start_year ] ; then
      # write header
      echo -e 'year\torigin\tdestination\t$prod_id\texport_val\timport_val' | bzip2 > year_origin_destination_$file_suffix.tsv.bz2
    fi
    
    mysql -B -N -D oec -h $OEC_DB_HOST -u macro -p$OEC_DB_PW -e "select year, substring(origin_id, 3) as origin, substring(dest_id, 3) as destination, substring($1_id, 3) as $prod_id, IFNULL(export_val, ''), IFNULL(import_val, '') from $1_yodp where year=$i $xtra_mysql order by origin, destination, $prod_id" | bzip2 >> year_origin_destination_$file_suffix.tsv.bz2
  done
done
