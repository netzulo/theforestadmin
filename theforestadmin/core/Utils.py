# -*- coding: utf-8 -*-
"""
Utils tasks
- files operations
- settings operations
"""


import json
import shutil
from sys import version_info
from os import path
from os import listdir
from os import makedirs


def path_format(file_path=None, file_name=None, is_abspath=False, ignore_raises=False):
    """
    Get path joined checking before if path and filepath exist,
     if not, raise an Exception
    """
    if not ignore_raises:
        if file_path is None or not path.exists(file_path):
            raise IOError("Path '{}' doesn't exists".format(file_path))
        if file_name is None or not path.exists("{}{}".format(file_path, file_name)):
            raise IOError("File '{}{}' doesn't exists".format(file_path, file_name))
        if is_abspath:
            return path.abspath(path.join(file_path, file_name))

    return path.join(file_path, file_name)

def read_file(is_json=False, file_path=None, encoding='utf-8', is_encoding=True):
    """Returns file object from file_path,
       compatible with all py versiones
    optionals:
      can be use to return dict from json path
      can modify encoding used to obtain file
    """
    text = None
    if file_path is None:
        raise Exception("File path received it's None")
    if version_info.major >= 3:
        if not is_encoding:
            encoding = None
        with open(file_path, encoding=encoding) as buff:
            text = buff.read()
    if version_info.major <= 2:
        with open(file_path) as buff:
            if is_encoding:
                text = buff.read().decode(encoding)
            else:
                text = buff.read()
    if is_json:
        return json.loads(text)
    return text

def settings():
    """Returns file settings as a dict to be use on qacode lib"""
    return read_file(is_json=True,
                     file_path=path_format(file_path='qacode/configs/',
                                           file_name='settings.json',
                                           is_abspath=True))



def force_merge_flat_dir(src_dir, dst_dir):
    """TODO"""
    if not path.exists(dst_dir):
        makedirs(dst_dir)
    for item in listdir(src_dir):
        src_file = path.join(src_dir, item)
        dst_file = path.join(dst_dir, item)
        force_copy_file(src_file, dst_file)

def force_copy_file(src_file, dst_file):
    """TODO"""
    if path.isfile(src_file):
        shutil.copy2(src_file, dst_file)

def is_flat_dir(src_dir):
    """TODO"""
    for item in listdir(src_dir):
        src_item = path.join(src_dir, item)
        if path.isdir(src_item):
            return False
    return True

def copy_tree(src, dst):
    """Allows to copy recursively and overwrite directory"""
    for item in listdir(src):
        src_path = path.join(src, item)
        dst_path = path.join(dst, item)
        if path.isfile(src_path):
            if not path.exists(dst):
                makedirs(dst)
            force_copy_file(src_path, dst_path)
        if path.isdir(src_path):
            is_recursive = not is_flat_dir(src_path)
            if is_recursive:
                copy_tree(src_path, dst_path)
            else:
                force_merge_flat_dir(src_path, dst_path)
