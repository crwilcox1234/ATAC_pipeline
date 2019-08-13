while read line
do
   cp ../"$line"_500/idr-output/"$line"_combined.peaks-top-set.txt "$line"_500combined.peaks-top-set.txt
   cp ../"$line"_150/idr-output/"$line"_combined.peaks-top-set.txt "$line"_150combined.peaks-top-set.txt
done < R1_list
