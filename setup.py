##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name = "hostout.debian"
setup(
    name = name,
    version = "0.1",
    author = "Leonardo J. Caballero G.",
    author_email = "leonardocaballero@gmail.com",
    description = """Plugin for collective.hostout that bootstraps an debian host ready for hostout deployment""",
    license = "GPL",
    keywords = "buildout, fabric, deploy, deployment, server, plone, django, host, hosting",
    url='https://svn.plone.org/svn/collective/'+name,
    long_description=(
        read('README.txt')
        + '\n' +
        read('hostout', 'debian', 'README.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' 
        ),

    packages = find_packages(),
    include_package_data = True,
#    data_files = [('.', ['*.txt'])],
#    package_data = {'':('*.txt')},
    namespace_packages = ['hostout'],
    install_requires = ['zc.buildout',
                        'zc.recipe.egg',
                        'setuptools',
                        'collective.hostout',
                        ],
    entry_points = {'zc.buildout':['default = hostout.debian:Recipe'],
        'fabric': ['fabfile = hostout.debian.fabfile'],
                    },
    zip_safe = False,
    )
