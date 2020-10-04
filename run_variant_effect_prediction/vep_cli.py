"""
Description:
    Example script to run variant effect prediction.

Output:
    Writes prediction files (absolute difference scores) to output dir.

Usage:
    vep_cli.py <vcf> <reference-fasta> <output-dir> [--cuda]
    vep_cli.py -h | --help

Options:
    -h --help               Show this screen.

    <vcf>                   Input VCF file
    <reference-fasta>       Reference genome file
    <output-dir>            Output directory
"""
import os

from docopt import docopt

from selene_sdk.sequences import Genome
from selene_sdk.utils import load_path
from selene_sdk.utils import parse_configs_and_run
from selene_sdk import __version__


if __name__ == "__main__":
    arguments = docopt(
        __doc__,
        version=__version__)

    def run_config(config_yml, output_dir):
        configs = load_path(config_yml, instantiate=False)
        configs["model"]['file'] = os.path.abspath(
            os.path.join('..', 'models', 'heartenn.py'))
        reference_fa = Genome(arguments["<reference-fasta>"])
        configs["analyze_sequences"].bind(
                reference_sequence=reference_fa,
                use_cuda=arguments["--cuda"])
        configs["variant_effect_prediction"].update(
            vcf_files=[arguments["<vcf>"]],
            output_dir=output_dir)
        parse_configs_and_run(configs)

    hout = os.path.join(arguments["<output-dir>"], "human_model")
    os.makedirs(hout, exist_ok=True)
    run_config("./heart_human_parameters.yml", hout)

    mout = os.path.join(arguments["<output-dir>"], "mouse_model")
    os.makedirs(mout, exist_ok=True)
    run_config("./heart_mouse_parameters.yml", mout)

