#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pysendmail',
    version='1.0',
    description='Python Module/Script for Sending E-mail',
    author='Chaz Lever',
    author_email='pysendmail+github@chazlever.com',
    url='http://www.github.com/chazlever/pysendmail',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pysendmail = pysendmail:_main', ],
    },
    zip_safe=True,
)
