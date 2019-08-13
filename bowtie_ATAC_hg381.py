# this program can generate the mapping files for ATAC-seq using bowtie

import sys

infile = open("R1_list")   # the list of the single cell sequence data files

for line in infile:

	name = line.strip().split('\n')[0]

	out = open((name + "bowtie_hg38.sh"), "w")

	out.write("#! /bin/bash\n#$ -N %sbowtie_hg38\n#$ -pe openmp 24\n#$ -q sam,som,bio,pub64\n\n"%(name))
	out.write("java -jar /data/apps/trimmomatic/0.35/trimmomatic-0.35.jar ")
	out.write("PE %s_R1.fastq.gz %s_R2.fastq.gz "%(name,name))
	out.write("pe_%s_R1.fastq se_%s_R1.fastq.gz pe_%s_R2.fastq se_%s_R2.fastq.gz "%(name,name,name,name))
	out.write("ILLUMINACLIP:NexteraPE-PE.fa:2:30:8:4:true ")
	out.write("LEADING:20 TRAILING:20 ")
	out.write("SLIDINGWINDOW:4:17 MINLEN:30\n\n")
	out.write("#gunzip %s_R1.fastq.gz\n#gunzip %s_R2.fastq.gz\n\n"%(name,name))
	out.write("module load samtools/0.1.19\nmodule load python/2.7.2\nmodule load bowtie2/2.2.7\n\n")
	out.write("bowtie2 --very-sensitive --no-discordant  -X 2000  -k 10 -p 24 --un-conc %s_unaligned.fastq -x /share/samdata/rmurad/DrMomand/genome/bowtie2/chrM/chrM -1 pe_%s_R1.fastq -2 pe_%s_R2.fastq | samtools view -Sb - > %s_chrM.bam\n\n"%(name,name,name,name))
	out.write("bowtie2 --very-sensitive -X 2000 --no-discordant -k 10 -p 24 -x /share/samdata/rmurad/DrMomand/genome/bowtie2/hg38 -1 %s_unaligned.1.fastq -2 %s_unaligned.2.fastq | samtools view -Sb - > %s_mappings.bam\n\n"%(name,name,name))
	out.write("samtools view -b -q 225 %s_mappings.bam > %s_mappings.uniq.bam"%(name,name))
	out.close()


