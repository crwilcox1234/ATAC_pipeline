import sys
infile = open("R1_list")   # the list of the multiple sequence data files
for line in infile:
        name = line.strip().split('\n')[0]
        out = open((name + "sort_hg38.sh"), "w")

        out.write("#! /bin/bash\n#$ -N %ssort_hg38\n#$ -pe openmp 16\n#$ -q som,sam,bio,pub8i\n#$ -M crwilcox@uci.edu\n#$ -m be\n\n"%(name))
        out.write("module load samtools/1.3\nmodule load homer/4.7\nmodule load picard-tools/1.96\n\n")
        out.write("java -Xmx2g -jar /data/apps/picard-tools/1.96/SortSam.jar INPUT=%s_mappings.bam OUTPUT=%s_mappings.sorted.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT\n\n"%(name,name))
        out.write("java -Xmx2g -jar /data/apps/picard-tools/1.96/MarkDuplicates.jar INPUT=%s_mappings.sorted.bam OUTPUT=%s_mappings.sorted.picard.bam METRICS_File= %s_mappings.PCR_duplicates.trim REMOVE_DUPLICATES=true\n\n"%(name,name,name))
        out.write("samtools view -c -F 4 %s_mappings.sorted.picard.bam\n"%(name))
        out.close()
#%s_mappings.PCR_duplicates.trim tells you how many mapped reads as well as the percent duplicates removed

