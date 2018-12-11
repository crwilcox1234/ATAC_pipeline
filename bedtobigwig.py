python file
import sys

infile = open("R1_list")   # the list of the multiple sequence data files

for line in infile:
        name = line.strip().split('\n')[0]
        out = open((name + "bedtobw_hg38.sh"), "w")

        out.write("#! /bin/bash\n#$ -N %sbedtobw_hg38\n#$ -pe openmp 16\n#$ -q som,sam,bio,pub8i\n#$  -ckpt blcr\n#$ -l kernel=blcr\n#$ -r y\n\n"%(name)
        out.write("module load bowtie/1.0.0\nmodule load samtools/1.3\nmodule load bedtools/2.19.1\nmodule load blat/35\nmodule load bedtools/2.25.0\n\n
        out.write("sortBed -chrThenSizeD -i %s_merge_final1.bed\n\n"%(name))
        out.write("bedtools getfasta -fi /som/crwilcox/hg38/hg38.fa -bed %s_merge_final1.bed -fo %s_merged.fa\n\n"%(name,name))
        out.write("bedtools genomecov -ibam %s_mappings.sorted.picard.bam -g %s_merged.fa -bga -scale 0.1710786 > %s_merged.bedGraph\n"%(name,name,name))
        out.write("bedGraphToBigWig %s_merged.bedGraph /som/crwilcox/hg38/chromesizes.txt %s_merged.bw\n"%(name,name))
        out.close()

