while read line
do
   awk -v OFS='\t' '{print $2,$3,$4}' "$line"_150combined.peaks-top-set.txt | tail -n+2 | LC_COLLATE=C sort -k1,1 -k2,2n > "$line"_150combined.peaks-top-set.bed
   awk -v OFS='\t' '{print $2,$3,$4}' "$line"_500combined.peaks-top-set.txt | tail -n+2 | LC_COLLATE=C sort -k1,1 -k2,2n > "$line"_500combined.peaks-top-set.bed
done < R1_list
