#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


def getversion():
    if 'BUILD_VERSION' in os.environ:
        return os.environ['BUILD_VERSION']
    else:
        return "0.0.5"


setup(
    name='pytest-nunit',
    version=getversion(),
    author='Anthony Shaw',
    author_email='anthonyshaw@apache.org',
    maintainer='Anthony Shaw',
    maintainer_email='anthonyshaw@apache.org',
    license='MIT',
    url='https://github.com/tonybaloney/pytest-nunit',
    description='A pytest plugin for generating Nunit3 test result XML output',
    long_description=read('README.rst'),
    py_modules=['pytest_nunit'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.5.0', 'enum34==1.1.6; python_version <= "3.4"', 'attrs'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'nunit = pytest_nunit.plugin',
        ],
    },
)
