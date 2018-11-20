#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='BSA Toolbelt',
    version='0.1',
    packages=find_packages(),
    package_data={'bsatoolbelt': ['sqls/*.sql']},
    install_requires=['records', 'psycopg2-binary', 'SQLAlchemy', 'requests'],
    keywords='toolbelt bsa business science analytics',
    url='https://github.com/olist/bsa-toolbelt',
    classifiers=['Development Status :: 3 - Alpha', 'Programming Language :: Python :: 3.6'],
    author='Andre Sionek',
    author_email='andre.sionek@olist.com',
    description='Toolbelt for everyday work and scripts done by the BS&A team'
)