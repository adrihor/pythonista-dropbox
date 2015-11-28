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
    'cffi==1.3.1',
    'cryptography==1.1.1',
    'decorator==4.0.4',
    'dropbox==3.42,',
    'enum34==1.0.4',
    'idna==2.0',
    'ipaddress==1.0.15',
    'ipython==4.0.1',
    'ipython-genutils==0.1.0',
    'ndg-httpsclient==0.4.0',
    'path.py==8.1.2',
    'pexpect==4.0.1',
    'pickleshare==0.5',
    'ptyprocess==0.5',
    'py==1.4.31',
    'pyasn1==0.1.9',
    'pycparser==2.14',
    'pyOpenSSL==0.15.1',
    'pytest==2.8.3',
    'requests==2.8.1',
    'simplegeneric==0.8.1',
    'six==1.10.0',
    'traitlets==4.0.0',
    'urllib3==1.12',
    'wheel==0.24.0',
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
