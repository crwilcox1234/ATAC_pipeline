# This program generates mapping files using bowtie2 for ATAC-seq

import sys

infile = open("R1_list") # the list of file names that need to be generated as mapping scripts

for line in infile:
  name = line.strip().split('\n')[0]
  
  out = open((name + "bowtie2_hg38.sh"), "w")
  
  out.write("#! /bin/bash\n#$ -N %sbowtie2_hg38\n#$ -pe openmp 8\n#$ -q sam,bio,pub64,pub8i\n\n"%(name))
  out.write("gunzip %s_R1.fstq.gz\ngunzip %s_R2.fastq.gz\n\n"%(name,name))
  out.write("module load samtools/0.1.19\nmodule load python/2.7.2\nmodule load bowtie2/2.2.7\n\n")
  out.write("bowtie2 --local -X 2000 -k3 -p 8 --un-conc %s_unaligned.fastq -x /share/samdata/rmurad/DrMomand/genome/bowtie2/chrM/chrM -1 %s_R1.fastq -2 %s_R2.fastq | samtools view -Sb -> %s_chrM.bam\n\n"%(name,name,name,name))
  out.write("bowtie2 --no-discordant -X 2000 --local -k 3 -p 8 -x /share/samdata/rmurad/DrMomand/genome/bowtie2/hg38 -1 %s_unaligned.1.fastq -2 %s_unaligned.2.fastq | samtools view -SB -> %s_mappings.bam\n\n"%(name,name,name))
  out.write("samtools view -b -q 30 %s_mappings.bam > %s_mappings.uniq.bam"%(name,name))
  out.close()
