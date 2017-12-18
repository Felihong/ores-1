"""
Runs a celery worker process that exposes a task API for
ores.scoring_systems.CeleryQueue

Usage:
    celery [--config-dir=<path>]... [--logging-config=<path>]
           [--debug] [--verbose]

Options:
    -h --help                Prints this documentation
    --config-dir=<path>      The path to a directory containing configuration
                             [default: config/]
    --logging-config=<path>  The path to a logging configuration file
    --debug                  Print debug logging information
    --verbose                Print verbose extraction information
"""
import logging

import docopt

from ..scoring_systems import CeleryQueue
from .util import build_config, configure_logging


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    verbose = args['--verbose']
    debug = args['--debug']

    run(verbose, debug,
        logging_config=args['--logging-config'],
        config_dirs=args['--config-dir'])


def run(verbose, debug, logging_config=None, **kwargs):
    configure_logging(logging_config)

    application = build(**kwargs)
    application.worker_main(
        argv=["celery_worker"])


def build(*args, **kwargs):
    config = build_config(*args, **kwargs)
    scoring_system = CeleryQueue.from_config(
        config, config['ores']['scoring_system'])
    return scoring_system.application
