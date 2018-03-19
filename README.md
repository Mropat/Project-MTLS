# Project in 3-state protein structure prediction with STRIDE

### This repository contains following scripts:

##### - Sequence-only prediction workflow
###### ....all_scripts/python/Sequence/
##

 > Extract sequence and structure infromation from 3-line  *.fasta files 

 > Encode sequence information with either BLOSUM or OneHotEncoding

 > Train models, view cross-validation performance reports and confusion plots

 > Read 2-line *.fasta files and output predictions based on a selection of trained models

#
#
#



##### - PSSM - based prediction workflow
######    ...all_scripts/python/PSSM/
##
> Split 3-line  *.fasta files in preparation of PSI-BLAST processing

> Bash script for PSI-BLAST query of the split files

> Extract and scale Substitution or Frequency matrices from *.PSSM files and save them to a dictionary

> Train and save final optimized models on PSSM data

> Train on adjustible proportion of total dataset over a range of window sizes, print cross-validation performance reports and show confusion plots

> Test saved models on adjustible proportion of our own testing dataset, print performance report and show confusion plot

#
#
#
##### - Misc processing
###### ...all_scripts/python/50_proteins/
##
> Run longest common substring on datasets in *.fasta format, print the IDs and save the list for exclusion

> Stride parser that creates 8-state, 3-line  *.fasta files from ALL chains in *.stride output files

> Stride parser that creates (A-type) 3-state, 3-line *.fasta files from ONE chain in *.stride output files





##### - Working models
##
###### Linear SVC predictor:
###### ...complete_predictors/Sequence_only/LinearSVC_21/ 
##
> Can be run locally from the folder on file named "testset.txt" :




##
###### PSSM-based predictor:
###### ...complete_predictors/PSSM_21/
#
> Should be run from project folder:

>  runs on the pssm file in the same folder (specified by name), modify name of file and choose another model if needed






###### BLOSUM-based predictor:
###### ...complete_predictors/BLOSUM_21/BLOSUM_predict.py
##
>Should be run from project folder, currently predicts on 50 first sequences from Stride testset, change if needed

#
#
#

##### - Saved optimized models to choose from:
###### ...models/
>  extract the rbfsvc_15 & rbfsvc_21 before running... 
##
##
##### If neeeded, run one of the hefty  .../all_scripts/python/PSSM/classifiers/ for better models and predictions
