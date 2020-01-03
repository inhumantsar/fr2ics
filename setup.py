#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as reqs_file:
    reqs = reqs_file.readlines()


setup(
    author="Shaun Martin",
    author_email='shaun@samsite.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="ugh excel spreadsheets",
    entry_points={
        'console_scripts': [
            'fr2ics=fr2ics.cli:main',
        ],
    },
    install_requires=reqs,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fr2ics',
    name='fr2ics',
    packages=find_packages(include=['fr2ics']),
    setup_requires=reqs,
    test_suite='test',
    url='https://github.com/inhumantsar/fr2ics',
    version='0.1.0',
    zip_safe=False,
)
