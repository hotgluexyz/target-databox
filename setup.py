#!/usr/bin/env python

from setuptools import setup

setup(
    name='target-databox',
    version='1.0.0',
    description='hotglue target for exporting data to Databox API',
    author='hotglue',
    url='https://hotglue.xyz',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['target_databox'],
    install_requires=[
        'databox==2.1.4',
        'pandas==1.1.3',
        'gluestick==1.0.4',
        'argparse==1.4.0'
    ],
    entry_points='''
        [console_scripts]
        target-databox=target_databox:main
    ''',
    packages=['target_databox']
)
