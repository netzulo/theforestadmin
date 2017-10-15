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
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from theforestadmin.core.Utils import copy_tree
from theforestadmin.core.Utils import read_file


EXE_NAME = 'TheForestDedicatedServer.exe'


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
    # LOADED
    server_path = config['server_path']
    params = [EXE_NAME]
    msg_deploy = "New server ready at'{}'".format(server_path)

    if args.deploy:
        cmd_deploy(config=config, logger=logger)
        logger.info(msg_deploy)
    if args.start:
        for param in config['options']:
            params.extend(' {}'.format(param))
        # START
        logger.info('CMD: cd %s', server_path)
        os.chdir(server_path)
        logger.info('CMD: %s', "".join(params))
        subprocess.call(params)


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
        custom_path = 'modules/{}/{}'.format(
            module['name'], 'Bundles/TheForest/')
        # just message templates
        msg_disabled = 'Disabled module: {}'.format(module['name'])
        msg_enabled = 'Enabled module: {}'.format(module['name'])
        msg_copy_module = "copy: from={} to={}".format(
            module_path, config['server_path'])
        msg_copy_custom = "copy: from={} to={}".format(
            custom_path, config['server_path'])
        # modules logic
        if not module['enabled']:
            logger.warning(msg_disabled)
        else:
            logger.info(msg_enabled)
            if module['name'] == 'Steam':
                logger.debug(msg_copy_module)
                copy_tree(module_path, config['server_path'])
            if module['name'] == 'Oxide':
                if module['custom']:
                    logger.debug(msg_copy_custom)
                    copy_tree(custom_path, config['server_path'])
                else:
                    # TODO: test code first
                    # stable builds steps:
                    # download
                    #import wget
                    #wget.download(url, out='path/path/')
                    # unzip
                    #import zipfile
                    # move to SERVER_PATH
                    #with zipfile.ZipFile("file.zip","r") as zip_ref:
                    #zip_ref.extractall("target_dir")
                    #copy_tree("target_dir", config['server_path'])
                    pass
            if module['name'] == 'Plugins':
                shutil.copy2(module_path, config['server_path'])

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
