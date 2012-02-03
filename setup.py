#!/usr/bin/env python

from setuptools import setup, find_packages

def get_version():
    from pysendmail import __version__
    return __version__

setup(
    name='pysendmail',
    version=get_version(),
    description='Python Module/Script for Sending E-mail',
    author='Chaz Lever',
    author_email='github+pysendmail@chazlever.com',
    url='http://www.github.com/chazlever/pysendmail',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pysendmail = pysendmail:_main', ],
    },
    zip_safe=True,
)
