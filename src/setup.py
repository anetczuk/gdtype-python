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

install_reqs = read_list( os.path.join( SCRIPT_DIR, "requirements.txt" ) )


setup( name='gdtype',
       version='2.0',
       description="Serialize and deserialize Godot's GDScript types in Python",
       url="https://github.com/anetczuk/gdtype-python",
       packages = packages_list,
       install_requires = install_reqs
     )
