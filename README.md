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
- Make sure you have `numpy`, `cython`, and `docopt` installed in your conda environment. (I've included a `heartenn-env.yml` example conda spec file that you can try using, but in practice I've found environment YAML files aren't easy to use out-of-the-box.)
- Build Selene: `python setup.py build_ext --inplace`
- Locally install Selene: `python setup.py install`

## Run variant effect prediction
- We've included the VCF files analyzed in the HeartENN publication in the directory `./run_variant_effect_prediction/data`. These are specified in hg19 coordinates, so you should download and use an hg19 FASTA as input into `vep_cli.py` for all of these VCFs. For example:
```
cd run_variant_effect_prediction
python ./vep_cli.py ./data/dnvs.vcf <path-to-file>/hg19.fa ./output
```
Add the `--cuda` flag if you can run the script on a CUDA-enabled GPU. It will take substantially longer on CPU (should only take a few mins to run on a GPU node). 

After `vep_cli.py` successfully runs, you will see two different output directories within `output`: `human_model` and `mouse_model`. This is because HeartENN includes both chromatin features measured in human and mouse, for which the training is done separately. The generated `.ref` and `.alt` files in these directories are the separate `ref` and `alt` sequence predictions, which are used to compute the `abs_diffs.tsv` file of variant effect predictions (`|alt - ref|`). 

### How to use the output
To use the results the way we did so in the HeartENN publication, combine the predictions for human and mouse into a single TSV. Example code snippet:

```
import pandas as pd

HMODEL_FILE = <path to human_model/*abs_diff.tsv>
MMODEL_FILE = <path to mouse_model/*abs_diff.tsv>

hdf = pd.read_csv(HMODEL_FILE, sep='\t')
mdf = pd.read_csv(MMODEL_FILE, sep='\t')
hdf = hdf.set_index(['chrom', 'pos', 'name', 'ref', 'alt'])
mdf = mdf.set_index(['chrom', 'pos', 'name', 'ref', 'alt'])

combined_df = pd.concat([hdf, mdf], axis=1)
```

Note that the HeartENN chromatin profile names do not specify mouse vs human, so you could update the `hdf` and `mdf` column names to distinguish between the two if desired.

The 'HeartENN score' is the max `abs_diff` value across all chromatin features for each variant. 

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
