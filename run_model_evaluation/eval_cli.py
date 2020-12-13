"""
Description:
    Example script to run model evaluation.

Output:
    Writes performance files to output dir.

Usage:
    eval_cli.py <config> <reference-fasta> <output-dir> [--cuda]
    eval_cli.py -h | --help

Options:
    -h --help               Show this screen.

    <config>                Configuration YAML file
    <reference-fasta>       Reference genome FASTA file
    <output-dir>            Output directory
    --cuda                  Use CUDA-enabled GPU
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

    configs = load_path(arguments["<config>"], instantiate=False)
    configs["model"]['path'] = os.path.abspath(
        os.path.join('..', 'heartenn.py'))

    reference_fa = Genome(arguments["<reference-fasta>"])
    configs["sampler"].bind(reference_sequence=reference_fa)

    configs["evaluate_model"].bind(use_cuda=arguments["--cuda"])

    configs["output_dir"] = arguments["<output-dir>"]

    parse_configs_and_run(configs)

