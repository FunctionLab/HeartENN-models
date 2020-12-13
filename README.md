# HeartENN

This repository supports the HeartENN models published with the Richter et al. (2020) publication, [_Genomic analyses implicate noncoding de novo variants in congenital heart disease_](https://doi.org/10.1038/s41588-020-0652-z).

# Setup

If you are interested in running HeartENN to make additional predictions, we recommend HeartENN models be used with Selene version 0.0.0 (already specified as a submodule for this repository). To use this repository along with the specified version of Selene, you can run 
```
git clone --recursive git@github.com:FunctionLab/HeartENN-models.git
```
(If you have problems loading the Selene submodule in this way, you can instead manually clone and load [this branch](https://github.com/kathyxchen/selene/tree/heartenn-branch-0.0.0) of Selene, which contains [one modification](https://github.com/kathyxchen/selene/commit/512dc4d7d194059a97fa8fdeffed5b8bbe2bafe1) to the original release that allows users to load these models with newer versions of PyTorch.)

If you only need to make comparisons against the predictions published in the manuscript, we recommend downloading the full set directly from [this Zenodo record](https://doi.org/10.5281/zenodo.4065588). 

Please post in the Github issues or e-mail Kathy Chen (kc31@princeton.edu) directly with any questions. Note that this repository is still a work-in-progress, with minimal instructions for getting started. We are happy to work with you by email until everything is stable and all documentation is pushed. 

# Getting started
- Make sure you have `numpy`, `cython`, and `docopt` installed in your conda environment.
- Build Selene: `python setup.py build_ext --inplace`
- Locally install Selene: `python setup.py install`

## Run variant effect prediction
- `cd run_variant_effect_prediction` and run `python ./vep_cli.py <vcf> <reference-fasta> <output-dir> [--cuda]`. We've included the VCF files analyzed in the HeartENN publication in the directory `./run_variant_effect_prediction/data`. These are specified in hg19 coordinates, so you should download and use an hg19 FASTA as input into `vep_cli.py` for all of these VCFs. For example:
```
python ./vep_cli.py ./data/dnvs.vcf <path-to-file>/hg19.fa ./output
```

## Run model evaluation 
- You will need to download hg19 and mm9 FASTA files and specify these paths (depending on which HeartENN model you run the evaluation on) as input to the `eval_cli.py` script.
- Example command: 
```
cd run_model_evaluation
python ./eval_cli.py ./heartenn1_mouse_eval.bed.yml 
                   <path-to-file>/mm9.fa
                   ./mouse_eval_outputs
                   --cuda
```

## Additional notes
- Please note that the Python scripts and configuration YAML files included in these repositories contain a number of relative path specifications, in Linux-style paths. These must be updated if you move this directory outside of its original source download.
- For model evaluation: the configuration files specify as input the `*_testset.selene.bed` files. These are generated using Selene's [IntervalsSampler](http://selene.flatironinstitute.org/overview/cli.html#intervals-sampler), where each row in the BED file is the input sequence coordinates (in hg19 or mm9, respectively) and the chromatin feature classes measured in that sequence (semicolon-separated, each number is the 0-indexed row number in the model's chromatin features file).
