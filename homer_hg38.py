import sys
infile = open("R1_list")   # the list of the single cell sequence data files
for line in infile:
        name = line.strip().split('\n')[0]
        out = open((name + "homer_mammal.sh"), "w")

        out.write("#! /bin/bash\n#$ -N %s_merge\n#$ -pe openmp 12\n#$ -q som,sam,bio,pub8i\n#$ -M crwilcox@uci.edu\n#$ -m be\n\n"%(name))
        out.write("module load samtools/1.3\nmodule load homer/4.7\nmodule load python/2.7.2\nmodule load picard-tools/1.96\n\n")
        out.write("mkdir %s_ATAC_tagdir150\nmkdir %s_ATAC_tagdir500\n\n"%(name,name))
        out.write("makeTagDirectory %s_ATAC_tagdir150 /dfs1/bio/crwilcox/MLSS2pooled/donovan/ATAC/ATAC_6_24h_092018/%s_mappings.shifted_reads.bam -format sam\n"%(name,name))
        out.write("findPeaks %s_ATAC_tagdir150 -o /dfs1/bio/crwilcox/MLSS2pooled/donovan/ATAC/ATAC_6_24h_092018/%s_ATAC_tagdir150.txt -style factor -size 150\n\n"%(name,name))
        out.write("makeTagDirectory %s_ATAC_tagdir500 /dfs1/bio/crwilcox/MLSS2pooled/donovan/ATAC/ATAC_6_24h_092018/%s_mappings.shifted_reads.bam -format sam\n"%(name,name))
        out.write("findPeaks %s_ATAC_tagdir500 -o /dfs1/bio/crwilcox/MLSS2pooled/donovan/ATAC/ATAC_6_24h_092018/%s_ATAC_tagdir500.txt -style factor -size 500 -minDist 50"%(name,name))
        out.close()

