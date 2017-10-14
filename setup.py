# -*- coding: utf-8 -*-
"""Installer and setup for theforestadmin"""


from os import path
from os import getcwd
from setuptools import setup, find_packages
from theforestadmin.core.Utils import read_file


CURR_PATH = path.abspath(path.join(getcwd()))
SCRIPTS_PATH = path.join(CURR_PATH, 'theforestadmin/scripts/')


setup(name='theforestadmin',
      version='0.0.0',
      packages=find_packages(exclude=['tests', 'modules']),
      description='TheForestAdmin, proyect manager for TheForest Game',
      long_description=read_file(file_path='README.rst'),
      author='Netzulo Open Source',
      author_email='netzuleando@gmail.com',
      url='https://github.com/netzulo/theforestadmin',
      download_url='https://github.com/netzulo/theforestadmin/tarball/v0.0.0',
      keywords=[
          'theforest',
          'game',
          'unity',
      ],
      install_requires=[
          'appdirs',
          'packaging==16.8',
          'pyparsing',
          'six==1.10.0',
          'nose==1.3.7',
          'nose-testconfig==0.10',
      ],
      scripts=[
          'theforestadmin/scripts/server.py',
      ]
     )
