# HeartENN

This repository supports the HeartENN models published with the Richter et al. (2020) publication, [_Genomic analyses implicate noncoding de novo variants in congenital heart disease_](https://doi.org/10.1038/s41588-020-0652-z).

# Setup

If you are interested in running HeartENN to make additional predictions, we recommend HeartENN models be used with Selene version 0.0.0. Specifically, you can clone and load [this branch](https://github.com/kathyxchen/selene/tree/heartenn-branch-0.0.0) of Selene, which contains [one modification](https://github.com/kathyxchen/selene/commit/512dc4d7d194059a97fa8fdeffed5b8bbe2bafe1) to the original release that allows users to load these models with newer versions of PyTorch.

If you only need to make comparisons against the predictions published in the manuscript, we recommend downloading the full set directly from [this Zenodo record](https://doi.org/10.5281/zenodo.4065588). 

Please post in the Github issues or e-mail Kathy Chen (kc31@princeton.edu) directly with any questions. Note that this repository is still a work-in-progress, with minimal instructions for getting started. We are happy to work with you by email until everything is stable and all documentation is pushed. 

# Getting started

- Build Selene (make sure you are on the correct version/branch) with the instructions specified [here](https://github.com/FunctionLab/selene#installing-selene-from-source).
- You can either install the package locally `python setup.py install` in your conda environment or add a symlink `ln -s <path-to-selene_sdk>` in the directory `run_variant_effect_prediction`
- `cd run_variant_effect_prediction` and run `python ./vep_cli.py <vcf> <reference-fasta> <output-dir> [--cuda]`. We've included the VCF files analyzed in the HeartENN publication in the directory `./run_variant_effect_prediction/data`. These are specified in hg19 coordinates, so you should download and use an hg19 FASTA as input into `vep_cli.py` for all of these VCFs. 
