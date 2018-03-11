cd project/Project-MTLS/all_scripts/python/PSSM_in

export BLASTDB=/local_uniref/uniref/uniref90

for f in *; do if [ ! -f ../PSSM_out/$f.psiblast ]; then psiblast -query $f -db uniref90.db -num_iterations 3 -evalue 0.001 -out ../PSSM_out/$f.psiblast -out_ascii_pssm ../PSSM_out/$f.pssm -num_threads 8; fi; done





