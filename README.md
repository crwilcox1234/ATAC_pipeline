ATAC Pipeline
=============

1. First use bowtie to map reads to respective genome, script is called: bowtie_atac.py 
2. Then use picard tools to remove PCR duplicates and sort.  script is called: PCR_duplicates.py
3. Third, shift peaks before calling peaks. Script is called shift.reads.py
### Use the command line below to run shift.reads.py

```bash
samtools view mappings.nodup.bam | python /dfs1/bio/crwilcox/ATAC_pooled/afterMarkDuplicates/shift.reads.py  shifted_reads.sam
```

### The shifted_reads.sam file needs to be converted into a bam file, so you will need a bamheader file for your specific genome.  Then use the script below
```bash
cat /dfs1/bio/crwilcox/ATAC_pooled/hg38_bamHeader.sam shifted_reads.sam | samtools view -Sb - > shifted_reads.bam
```

4. After shifting reads cn now run peak calling.  I use homer for this with the script named: homer_hg38.py
### This script includes script for finding peaks for 150bp and 500bp length reads

5. After homer remove the homer header and remove some columns to make a .bed file
```bash
awk 'NR>34' filename.txt > new_filename.txt
awk -v OFS='\t' '{print$2,$3,$4,$5}' DnAtac_24_3_ATAC_tagdir150_noheader.txt > DnAtac_24_3_ATAC_tagdir150.bed
```

6. You need to memove the header using the script:
If you remove the header this way, skip step 7. It becomes irrelevant 
```bash
awk 'NR>1' filename_500.bed > filename_500_1.bed
```
Then merge the 150bp and 500bp .bed files: merge_hg38.py

7. Take out the first 4 lines of the file. Also the first line is usually only "hr", so have to add a "c" to make it "chr"
```bash
awk 'NR>4' filename_merge_final.bed > filename_merge_final1.bed
```
8. Now need to visualize the files on the Genome browser (UCSC or IGV). Use this script: bedtobigwig.py
### You will need chromsizes.txt, but you can make one in anaconda environment using the script
```
faidx input.fasta -i chromsizes > sizes.genome
```
#### pyfaidx is already installed, just need to run it with anaconda

9. To get # reads in peaks: (bed file must be sorted first):
```
sort -k1,1 -k2,2n filename.bed > newfilename.bed
coverageBed -abam ../shift_reads/H0_1ATAC_S27_shifted_reads.bam -b H0_1ATAC_S27_merge_final.bed > H0_coverage.bed
```
10. The next thing is to run IDR to remove peaks that are not reproducible 

NOTE: if you use a genome with chromosome names without 'chr' before the numbers, you need to go into the utils.py file and remove the chr infront of chr[x] and the below statement.

## Now use the idr-pipline.py listed above in the scripts.  Makes multiple idr scripts based on an R1_list.
## idr-pipline.py is based off of the pipline below

```bash
10.	###RUN IDR PIPELINE#### 
#! /bin/bash
#$ -N entire.IDR.run
#$ -pe openmp 1
#$ -q sam,bio,som
```
```
module load R/3.4.1
module load bowtie/1.0.0
module load samtools/1.3
module load homer/4.7
module load picard-tools/1.96
#module load R/3.1.3
# ------------------------------------------------------------------------------------------------
# Note:
# ------------------------------------------------------------------------------------------------
# IDR code runs only with python3. Use Anaconda3 python by setting path in the .bashrc file
# ------------------------------------------------------------------------------------------------
# Copy required scripts and code to this folder
# ------------------------------------------------------------------------------------------------
cp -r /share/samdata/rmurad/DrMomand/code/idr-code/homer-idr/idr/* .
# ------------------------------------------------------------------------------------------------
# Copy the peaks for each replicate into one folder
# ------------------------------------------------------------------------------------------------
mkdir -p peaks/replicates/
cp ../../../needed_files/AS1_1_ATAC_tagdir200.txt peaks/replicates/
cp ../../../needed_files/AS1_2_ATAC_tagdir200.txt peaks/replicates/
cp ../../../needed_files/AS1_3_ATAC_tagdir200.txt peaks/replicates/
# ------------------------------------------------------------------------------------------------
# Make a combined tag directory for all reps, find peaks for pooled combined
# ------------------------------------------------------------------------------------------------
#makeTagDirectory Combined -d /share/samdata/rmurad/DrMomand/omATAC/br/br4/homer-tags /share/samdata/rmurad/DrMomand/omATAC/br/br5/homer-tags
makeTagDirectory Combined -d ../../../AS1_1_ATAC_tagdir200 ../../../AS1_2_ATAC_tagdir200 ../../../AS1_3_ATAC_tagdir200
cd Combined
findPeaks ./ -LP .1 -poisson .1 -style factor -size 200 -minDist 50 -localSize 50000 -o combined.peaks.txt
cd ../
# ------------------------------------------------------------------------------------------------
# Create pseudoreps for individual reps (Step 5)
# ------------------------------------------------------------------------------------------------
mkdir -p pseudoreps/individual
#python run_idr.py pseudoreplicate -d /share/samdata/rmurad/DrMomand/omATAC/br/br4/homer-tags /share/samdata/rmurad/DrMomand/omATAC/br/br5/homer-tags -o pseudoreps/individual
python run_idr.py pseudoreplicate -d ../../../AS1_1_ATAC_tagdir200 ../../../AS1_2_ATAC_tagdir200 ../../../AS1_3_ATAC_tagdir200 -o pseudoreps/individual
# ------------------------------------------------------------------------------------------------
# Create pseudoreps for pooled (Step6)
# ------------------------------------------------------------------------------------------------
mkdir -p pseudoreps/pooled
python run_idr.py pseudoreplicate -d Combined -o pseudoreps/pooled
# ------------------------------------------------------------------------------------------------
# Call peaks for individual pseudoreps (Step 7)
# ------------------------------------------------------------------------------------------------
mkdir -p peaks/pseudoreps
cd peaks/pseudoreps
for f in ../../pseudoreps/individual/*
        do
        findPeaks $f -LP .1 -poisson .1 -style factor -size 200 -minDist 50 -localSize 50000 -o ${f}_peaks.txt
        done
cd ../../
# ------------------------------------------------------------------------------------------------
# Call peaks for combined pseudoreps (Step 8)
# ------------------------------------------------------------------------------------------------
mkdir -p peaks/pooled-pseudoreps
cd peaks/pooled-pseudoreps
for f in ../../pseudoreps/pooled/*
        do
        findPeaks $f -LP .1 -poisson .1 -style factor -size 200 -minDist 50 -localSize 50000 -o ${f}_peaks.txt
        done
cd ../../
# ------------------------------------------------------------------------------------------------
# Finally run IDR (Step 9)
# ------------------------------------------------------------------------------------------------
cp pseudoreps/individual/*peaks.txt peaks/pseudoreps/
cp pseudoreps/pooled/*peaks.txt peaks/pooled-pseudoreps/
python  run_idr.py idr \
        -p peaks/replicates/* \
        -pr peaks/pseudoreps/* \
        -ppr peaks/pooled-pseudoreps/* \
        --pooled_peaks Combined/combined.peaks.txt \
        -o idr-output \
        --threshold .01
```

11. Copy idr output for each sample and rename into a new directory
### Examples:

```bash
cp ../AS1/idr_500bp/idr-output/combined.peaks-top-set.txt AS1_500bp_topset.txt
```
### Or use the shell script cpnamechange.sh:

``` bash
while read line
do
   cp ../"$line"_500/idr-output/"$line"_combined.peaks-top-set.txt "$line"_500combined.peaks-top-set.txt
   cp ../"$line"_150/idr-output/"$line"_combined.peaks-top-set.txt "$line"_150combined.peaks-top-set.txt
done < R1_list
```

12. Convert IDR output to .bed format
```
awk -v OFS='\t' '{print $2,$3,$4}' AS1_200bp_topset.txt | tail -n+2 | LC_COLLATE=C sort -k1,1 -k2,2n > AS1_200bp_topset.bed
```

### Or use the shell script 

```bash
while read line
do
   awk -v OFS='\t' '{print $2,$3,$4}' "$line"_150combined.peaks-top-set.txt | tail -n+2 | LC_COLLATE=C sort -k1,1 -k2,2n > "$line"_150combined.peaks-top-set.bed
   awk -v OFS='\t' '{print $2,$3,$4}' "$line"_500combined.peaks-top-set.txt | tail -n+2 | LC_COLLATE=C sort -k1,1 -k2,2n > "$line"_500combined.peaks-top-set.bed
done < R1_list

``` 

13. merge all the peaks
```
cat AS2*.bed AS1*.bed | sort -k1,1 -k2,2n | bedtools merge > AS1_AS2_merged.peaks.bed
```

14. Find how many peaks overlap the ENCODE blacklist
```
bedtools intersect -a AS1_AS2_merged.peaks.bed -b /bio/rmurad/DrMomand/omATAC/analysis/encode-data/ENCODE_blacklisted_regions_hg38/hg38.blacklist.bed hg38.blacklist.bed -wo
```

15. Remove peaks overlapping ENCODE blacklist

```bash

bedtools intersect -v -a merged.peaks.bed -b hg38.blacklist.bed > merged.peaks.noENCODEblacklistedRegions.bed

```

16. Fix the filtered peaks bed file by adding 3 additional columns

### /share/samdata/rmurad/DrMomand/code/ is where you can get the addPeakName.py

```bash
python addPeakName.py AS1_AS2_merged.peaks.noENCODEblacklistedRegions.bed AS1_AS2_merged.peaks. noENCODEblacklistedRegions.fixed.bed
```

17. Convert the bed to bigBed

### have your own bedtoBigBed program, have the program directory before the name

```bash
bedToBigBed merged.peaks.noENCODEblacklistedRegions.fixed.bed hg38.chrom.sizes merged.peaks.noENCODEblacklistedRegions.fixed.bb

```

18. Annotate peaks using homer (annotatePeaks.pl)

```bash
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

```

19. You now have a counts matrix you can input into R to analyze
