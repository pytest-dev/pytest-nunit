#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import find_packages
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


def getversion():
    if 'BUILD_VERSION' in os.environ:
        return os.environ['BUILD_VERSION']
    else:
        return "1.0.0"


setup(
    name='pytest-nunit',
    version=getversion(),
    author='Anthony Shaw',
    author_email='anthonyshaw@apache.org',
    maintainer='Anthony Shaw',
    maintainer_email='anthonyshaw@apache.org',
    license='MIT',
    url='https://github.com/pytest-dev/pytest-nunit',
    description='A pytest plugin for generating NUnit3 test result XML output',
    long_description=read('README.rst'),
    packages=find_packages(exclude=('test*',)),
    python_requires='>=3.6',
    install_requires=['pytest>=4.6.0', 'attrs'],
    extras_require={
        ':python_version=="2.7"': ['enum34>=1.1.6'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
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
