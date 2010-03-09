# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009 by:
#     * Robert Barsch
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

"""
setup.py bdist_egg
"""

from setuptools import setup


setup(
    name='seishub.plugins.seismology',
    version='0.0.1',
    description="",
    long_description="""""",
    classifiers=[],
    keywords='',
    author='Robert Barsch',
    author_email='barsch@geophysik.uni-muenchen.de',
    url='https://svn.geophysik.uni-muenchen.de/svn/seishub',
    license='BSD',
    packages=['seishub.plugins.seismology'],
    namespace_packages=['seishub', 'seishub.plugins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points={'seishub.plugins': ['seishub.plugins.seismology = seishub.plugins.seismology', ]},
)
