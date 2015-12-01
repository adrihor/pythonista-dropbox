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
    'keyring',
]

test_requirements = [
    # TODO: put package test requirements here
    'pytest',
]
keys = ('run_command', 'app_directory')
commands = (
    'request-auth-token',
    'set-keychain',
)
app_directories = (
    'pythonista_dropbox.request_auth_token',
    'pythonista_dropbox.client_scripts.set_keychain',
)
format_kwargs = [
    dict(zip(keys, (command, app_directory)))
    for command, app_directory in zip(commands, app_directories)
]
entry_points = {
    'console_scripts': ['{run_command} = {app_directory}:main'.
                        format(**format_kwarg) for format_kwarg
                        in format_kwargs]
}

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
        'pythonista_dropbox/pythonista_modules',
        'pythonista_dropbox/client_scripts',
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
    tests_require=test_requirements,
    entry_points=entry_points
)
