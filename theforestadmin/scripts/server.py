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
from theforestadmin.core.Utils import copy_tree
from theforestadmin.core.Utils import read_file


EXE_NAME='TheForestDedicatedServer.exe'


def main(args=None):
    """TODO"""
    args, parser = before_cmd(args=args)    
    # START SCRIPT
    args = parser.parse_args()
    logger = get_logger(args=args)
    # START command handling
    config = None
    if args.config_path is None:
        config = read_file(is_json=True,
                           file_path='theforestadmin/configs/server.json')
    else:
        config = read_file(is_json=True, file_path=args.config_path)
    if config is None:
        raise Exception("Configuration can't be None")
    logger.info(config)
    if args.deploy:
        cmd_deploy(config=config, logger=logger)
    if args.start:
        params = []
        server_path = config['server_path']
        exe_path = "{}{}".format(server_path, EXE_NAME)
        for param in config['options']:
            params.extend(param['name'])
            params.extend(' ')
            params.extend(param['value'])
            params.extend(' ')
        logger.info("Starting server with params: {} {}"
                    "".format(exe_path, "".join(params)))
        subprocess.call(params)
    logger.info("Terminated execution")


def cmd_deploy(config=None, logger=None):
    """Deploy operations"""
    logger.info("Cloning modules...")
    modules = [
        config['modules']['steam'],
        config['modules']['oxide'],
        config['modules']['plugins']
    ]
    for module in modules:
        module_path = 'modules/{}'.format(module['name'])
        custom_path = 'modules/{}/{}'.format(module['name'], 'Bundles/TheForest/')        
        if not module['enabled']:
            logger.warning("Disabled module: {}".format(module['name']))
        else:
            logger.info('Apply module: {}'.format(module['name']))
            if module['name'] == 'Steam':
                logger.debug("copy: from={} to={}"
                             "".format(module_path, config['server_path']))
                copy_tree(module_path, config['server_path'])
            if module['name'] == 'Oxide':
                if module['custom']:
                    logger.debug("copy: from={} to={}".format(
                        custom_path, config['server_path']))
                    copy_tree(custom_path, config['server_path'])
                # TODO else: stable, descargar, descomprimir, y pegar en SERVER_PATH
            if module['name'] == 'Plugins':
                shutil.copy2(module_path, config['server_path'])
            logger.info('Applied module: {}'.format(module['name']))
    return None

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
    parser.add_argument('-d', '--deploy', action='store_true',
                        help='Deploy new server based on JSON config')
    parser.add_argument('-s', '--start', action='store_true',
                        help='Start server based on JSON config')
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
