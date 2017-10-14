# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""TODO"""

import argparse
import logging
import logging.handlers
import os
import sys
import shutil
import subprocess

from theforestadmin.core.Utils import read_file


def main(args=None):
    """TODO"""
    args, parser = before_cmd(args=args)    
    # START SCRIPT
    args = parser.parse_args()
    logger = get_logger(args=args)
    # START command handling
    config = None
    if args.config_path is None:
        config = read_file(is_json=True, file_path='theforestadmin/configs/server.json')
    else:
        config = read_file(is_json=True, file_path=args.config_path)
    if config is None:
        raise Exception("Configuration can't be None")
    logger.info(config)
    logger.debug("NO MORE ACTIONS IMPLEMENTED")


def before_cmd(args=None):
    """Generate logs folder, instance argparse and return it"""
    if args is None:
        args = sys.argv[1:]
    if not os.path.exists('logs'):
        os.mkdir('logs')
    parser = argparse.ArgumentParser(
        description="Performs TheForest server operations",
        epilog="----- help us on , https://github.com/netzulo/theforestadmin -------",
        fromfile_prefix_chars='@',)
    ## Main args
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Activate DEBUG level')
    parser.add_argument('-c', '--config_path', default=None,
                        help='Path for custom JSON config')
    return (args, parser,)

def get_logger(args=None):
    """TODO"""
    logger = logging.getLogger('theforestadmin')
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    # logger file
    log_file_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/theforestadmin.log', when='M', interval=2)
    log_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s](%(name)s:%(funcName)s:%(lineno)d): %(message)s'))
    log_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)
    # logger console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('[%(levelname)s](%(name)s): %(message)s'))
    logger.addHandler(console_handler)
    return logger


if __name__ == '__main__':
    main()
