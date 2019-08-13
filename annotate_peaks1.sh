#! /bin/bash
#$ -N DvnATAC0_1_S1_merge
#$ -pe openmp 1
#$ -q sam,som,bio,pub64

module load samtools/1.3
module load homer/4.7
module load python/2.7.2
module load perl
module load picard-tools/1.96

annotatePeaks.pl Dvn_0_6_24_48merged.peaks.noENCODEblacklistedRegions.fixed.bed \
hg19 -raw -annStats Dvn_0_6_24_48annotationStats.txt \
-d \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC0_1_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC0_2_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC0_3_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC6_1_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC6_2_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC6_3_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC24_1_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC24_2_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC24_3_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC48_1_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC48_2_ATAC_tagdir150/ \
/share/samdata/crwilcox/ATAC_pooled/Donovan/ATAC_1902/rename/DvnATAC48_3_ATAC_tagdir150/ \
> Dvn_0_6_24_48peak-tags.txt

cut -f 1,20,21,22,23,24,24,25,26,27,28 Dvn_0_6_24_48peak-tags.txt > Dvn_0_6_24_48counts.txt
