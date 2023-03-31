#!/usr/bin/env python3

import os

from setuptools import setup, find_packages


SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )


def read_list( file_path ):
    if not os.path.isfile( file_path ):
        return []
    ret_list = []
    with open( file_path, 'r', encoding='utf-8' ) as content_file:
        for line in content_file:
            ret_list.append( line.strip() )
    return ret_list


packages_list = find_packages( include=['gdtype', 'gdtype.*'] )

requirements_path = os.path.join( SCRIPT_DIR, "requirements.txt" )
install_reqs = read_list( requirements_path )

## every time setup info changes then version number should be increased

setup( name='gdtype',
       version='2.0.1',
       description="Serialize and deserialize Godot's GDScript types in Python",
       url="https://github.com/anetczuk/gdtype-python",
       author='anetczuk',
       license='MIT',
       packages=packages_list,
       install_requires=install_reqs
       )
