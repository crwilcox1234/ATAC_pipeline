# this program can generate the mapping files for ATAC-seq using bowtie

import sys

infile = open("R1_list")   # the list of the single cell sequence data files

for line in infile:

	name = line.strip().split('\n')[0]

	out = open((name + "bowtie_hg38.sh"), "w")

	out.write("#! /bin/bash\n#$ -N %sbowtie_hg38\n#$ -pe openmp 10\n#$ -q som,sam,bio,pub8i\n\n"%(name))
	out.write("module load bowtie/1.0.0/nmodule load samtools/0.1.19/nmodule load python/2.7.2\n\n") 
	out.write("bowtie -X 1500 --trim3 13 -a -S -p 8 -v 3  --un %s_unaln.fastq /som/crwilcox/hg38/chrM \
        -1 %s_R1.fastq -2 %s_R2.fastq | samtools view -Sb - > %s_temp.bam"%(name,name,name))
	out.write("bowtie -X 1500 --trim3 13 -m 3 -k 1 --best -S -p 8 -v 3 /som/crwilcox/hg38/hg38 -1 %s_unaln_1.fastq \
        -2 %s_unaln_2.fastq | samtools view -Sb - > %s_mappings.bam"%(name,name,name))
	out.close()


