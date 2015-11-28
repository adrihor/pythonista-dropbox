#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'dropbox==3.42,',
]

test_requirements = [
    # TODO: put package test requirements here
    'pytest',
]

setup(
    name='pythonista_dropbox',
    version='0.1.0',
    description="",
    long_description=readme + '\n\n' + history,
    author="Don M. Morehouse",
    author_email='dmmmdfll@gmail.com',
    url='https://github.com/dmorehousemd/pythonista_dropbox',
    packages=[
        'pythonista_dropbox',
    ],
    package_dir={'pythonista_dropbox':
                 'pythonista_dropbox'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pythonista_dropbox',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
