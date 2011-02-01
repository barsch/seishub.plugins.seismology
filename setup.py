#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
seishub.plugins.seismology installer

:copyright:
    Robert Barsch (barsch@lmu.de)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""

from setuptools import setup
import os


VERSION = open(os.path.join("seishub", "plugins", "seismology",
                            "VERSION.txt")).read()


setup(
    name='seishub.plugins.seismology',
    version=VERSION,
    description="Seismology package for SeisHub.",
    long_description="""
    seishub.plugins.seismology - Seismology package for SeisHub.

    For more information visit http://www.seishub.org.
    """,
    url='http://www.seishub.org',
    author='Robert Barsch',
    author_email='barsch@lmu.de',
    license='GNU Lesser General Public License, Version 3 (LGPLv3)',
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' + \
        'GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=['SeisHub', 'seismology'],
    packages=['seishub.plugins.seismology'],
    namespace_packages=['seishub', 'seishub.plugins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'seishub.core',
        'obspy.core',
        'obspy.mseed',
        'obspy.gse2',
        'obspy.seishub',
        'obspy.imaging',
        'obspy.xseed',
        'obspy.arclink',
        'obspy.db',
    ],
    dependency_links=[
        "https://svn.obspy.org/trunk/obspy.db#egg=obspy.db-dev"
    ],
    download_url="https://svn.geophysik.uni-muenchen.de/svn/seishub/trunk/seishub.plugins.seismology#egg=seishub.plugins.seismology-dev",
    entry_points={'seishub.plugins': [
        'seishub.plugins.seismology = seishub.plugins.seismology', ]
    },
)
