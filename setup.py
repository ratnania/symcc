# -*- coding: UTF-8 -*-
#! /usr/bin/python

import sys
from setuptools import setup

NAME    = 'symcc'
VERSION = '0.1'
AUTHOR  = 'Jim Crist, Ahmed Ratnani'
EMAIL   = 'ahmed.ratnani@ipp.mpg.de'
URL     = 'https://github.com/ratnania/symcc'
DESCR   = 'Symbolic Mathematics Compiler'
KEYWORDS = ['math']
LICENSE = "LICENSE"

setup_args = dict(
    name                 = NAME,
    version              = VERSION,
    description          = DESCR,
    long_description     = open('README.md').read(),
    author               = AUTHOR,
    author_email         = EMAIL,
    license              = LICENSE,
    keywords             = KEYWORDS,
    url                  = URL,
#    download_url     = URL+'/tarball/master',
)


# ...
packages=[  'symcc' \
          , 'symcc.dsl' \
          , 'symcc.printers' \
          , 'symcc.types' \
          , 'symcc.utilities' \
         ]

package_dir={  'symcc':                'symcc' \
              ,'symcc.dsl':            'symcc/dsl' \
              ,'symcc.dsl.gramar':     'symcc/dsl/grammar' \
              ,'symcc.printers':       'symcc/printers' \
              ,'symcc.types':          'symcc/types' \
              ,'symcc.utilities':      'symcc/utilities' \
              ,}
# ...


def setup_package():
    if 'setuptools' in sys.modules:
        setup_args['install_requires'] = ['numpy']
    setup(  packages = packages \
          , package_dir=package_dir \
          , include_package_data = True \
          , **setup_args)


if __name__ == "__main__":
    setup_package()
