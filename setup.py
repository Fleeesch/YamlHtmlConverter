#!/usr/bin/env python

from distutils.core import setup

setup(
    name='YamlHtmlConverter',
    version='1.0.0',
    author='Fleeesch',
    author_email='-',
    description='-',
    packages=['lib'],
    install_requires=['bs4', 'PyYAML','soupsieve', 'wheel'],
)