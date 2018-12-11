infile = open("R1_list")   # the list of the single cell sequence data files
for line in infile:
        name = line.strip().split('\n')[0]
        out = open((name + "merge200500_hg38.sh"), "w")

        out.write("#! /bin/bash\n#$ -N %s_merge\n#$ -pe openmp 2\n#$ -q som,sam,bio,pub8i\n\n\n"%(name))
        out.write("module load bedops/2.4.14\nmodule load samtools/1.3\nmodule load python/2.7.2\nmodule load picard-tools/1.96\n\n")
        out.write("bedops --merge %s_ATAC_tagdir150.bed %s_ATAC_tagdir500.bed > %s_merge_final.bed"%(name,name,name))
        out.close()

